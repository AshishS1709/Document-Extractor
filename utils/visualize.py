from typing import List, Dict, Tuple, Any, Optional
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import io

class DocumentVisualizer:
    """Visualizes document processing results with bounding boxes and annotations."""
    
    def __init__(self, font_path: Optional[str] = None, font_size: int = 12):
        """
        Initialize the visualizer with optional custom font.
        
        Args:
            font_path: Path to a .ttf font file. If None, uses default PIL font.
            font_size: Font size in points.
        """
        self.font_size = font_size
        try:
            self.font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except IOError:
            self.font = ImageFont.load_default()
    
    def draw_boxes_on_image(
        self,
        image: Image.Image,
        boxes: List[Dict[str, Any]],
        color: Tuple[int, int, int] = (0, 255, 0),
        line_width: int = 2,
        show_labels: bool = True,
        label_color: Tuple[int, int, int] = (0, 0, 255)
    ) -> Image.Image:
        """
        Draw bounding boxes on an image.
        
        Args:
            image: PIL Image to draw on
            boxes: List of box dictionaries with 'bbox' and 'label' keys
            color: RGB color for the boxes
            line_width: Width of the box borders
            show_labels: Whether to show labels
            label_color: Text color for labels
            
        Returns:
            PIL Image with drawn boxes
        """
        draw = ImageDraw.Draw(image)
        
        for box in boxes:
            # Get coordinates (convert to integers)
            x1, y1, x2, y2 = map(int, box['bbox'])
            
            # Draw rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)
            
            # Draw label if requested
            if show_labels and 'label' in box:
                label = str(box['label'])
                if 'confidence' in box:
                    label += f" ({box['confidence']:.2f})"
                
                # Draw text background
                text_bbox = draw.textbbox((x1, y1 - 20), label, font=self.font)
                draw.rectangle(text_bbox, fill=color)
                
                # Draw text
                draw.text((x1, y1 - 20), label, fill=label_color, font=self.font)
        
        return image
    
    def visualize_ocr_results(
        self,
        image: Image.Image,
        ocr_results: Dict[str, Any],
        show_boxes: bool = True,
        show_text: bool = True
    ) -> Image.Image:
        """
        Visualize OCR results on the original image.
        
        Args:
            image: Original PIL Image
            ocr_results: Dictionary containing OCR results
            show_boxes: Whether to draw bounding boxes
            show_text: Whether to draw recognized text
            
        Returns:
            PIL Image with visualization
        """
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        if 'text_boxes' in ocr_results:
            for box in ocr_results['text_boxes']:
                if show_boxes and 'bbox' in box:
                    x1, y1, x2, y2 = map(int, box['bbox'])
                    draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
                
                if show_text and 'text' in box and 'bbox' in box:
                    x1, y1, _, _ = map(int, box['bbox'])
                    draw.text((x1, y1 - 15), box['text'], fill='red', font=self.font)
        
        return img_copy
    
    def plot_histogram(
        self,
        data: List[float],
        title: str = "Distribution",
        xlabel: str = "Values",
        ylabel: str = "Frequency",
        bins: int = 20,
        color: str = 'skyblue',
        edgecolor: str = 'black'
    ) -> Image.Image:
        """
        Create a histogram plot and return as PIL Image.
        
        Args:
            data: List of numerical values
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            bins: Number of bins
            color: Bar color
            edgecolor: Bar edge color
            
        Returns:
            PIL Image of the plot
        """
        plt.figure(figsize=(8, 6))
        plt.hist(data, bins=bins, color=color, edgecolor=edgecolor, alpha=0.7)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        
        # Save plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        buf.seek(0)
        
        # Convert to PIL Image
        return Image.open(buf)
    
    def create_side_by_side(
        self,
        image1: Image.Image,
        image2: Image.Image,
        label1: str = "Original",
        label2: str = "Processed"
    ) -> Image.Image:
        """
        Create a side-by-side comparison of two images.
        
        Args:
            image1: First image
            image2: Second image
            label1: Label for the first image
            label2: Label for the second image
            
        Returns:
            Combined PIL Image
        """
        # Ensure both images have the same height
        max_height = max(image1.height, image2.height)
        
        # Resize images to have the same height
        img1 = image1.resize(
            (int(image1.width * max_height / image1.height), max_height),
            Image.Resampling.LANCZOS
        )
        img2 = image2.resize(
            (int(image2.width * max_height / image2.height), max_height),
            Image.Resampling.LANCZOS
        )
        
        # Create a new image with enough width for both images plus a border
        border = 10
        total_width = img1.width + img2.width + 3 * border
        combined = Image.new('RGB', (total_width, max_height + 40), 'white')
        
        # Paste images
        combined.paste(img1, (border, 30))
        combined.paste(img2, (img1.width + 2 * border, 30))
        
        # Add labels
        draw = ImageDraw.Draw(combined)
        text_y = 10
        
        # Draw first label
        text_bbox = draw.textbbox((0, 0), label1, font=self.font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = border + (img1.width - text_width) // 2
        draw.text((text_x, text_y), label1, fill='black', font=self.font)
        
        # Draw second label
        text_bbox = draw.textbbox((0, 0), label2, font=self.font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = img1.width + 2 * border + (img2.width - text_width) // 2
        draw.text((text_x, text_y), label2, fill='black', font=self.font)
        
        return combined

# Example usage:
if __name__ == "__main__":
    # Example of how to use the DocumentVisualizer
    visualizer = DocumentVisualizer()
    
    # Create a sample image
    width, height = 400, 300
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add some content to the image
    draw.rectangle([50, 50, 150, 150], outline='blue', width=2)
    draw.text((60, 60), "Sample Text", fill='black')
    
    # Define some boxes
    boxes = [
        {'bbox': [40, 40, 160, 160], 'label': 'Box 1', 'confidence': 0.95},
        {'bbox': [200, 100, 300, 200], 'label': 'Box 2', 'confidence': 0.87}
    ]
    
    # Draw boxes on the image
    result = visualizer.draw_boxes_on_image(image, boxes)
    
    # Save or display the result
    result.save("visualization.png")
    print("Visualization saved as 'visualization.png'")

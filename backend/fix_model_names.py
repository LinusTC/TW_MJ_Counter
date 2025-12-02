import torch
from pathlib import Path

def update_model_class_names(model_path, new_names_dict):
    """
    Update class names in a trained YOLO model
    
    Args:
        model_path: Path to the .pt model file
        new_names_dict: Dictionary mapping class IDs to new names
    """
    print(f"Loading model from: {model_path}")
    
    # Load the model checkpoint (weights_only=False for YOLO models)
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    
    # YOLO models have different structures, need to handle both
    if isinstance(checkpoint, dict):
        # Standard checkpoint format
        if 'model' in checkpoint:
            model_obj = checkpoint['model']
            # Check if model is a state dict or model object
            if hasattr(model_obj, 'names'):
                current_names = model_obj.names
                print(f"\nCurrent class names:")
                for idx, name in current_names.items():
                    print(f"  {idx}: {name}")
                
                # Update the names
                model_obj.names = new_names_dict
                
            elif isinstance(model_obj, dict) and 'names' in model_obj:
                current_names = model_obj['names']
                print(f"\nCurrent class names:")
                for idx, name in current_names.items():
                    print(f"  {idx}: {name}")
                
                # Update the names
                model_obj['names'] = new_names_dict
        
        # Also check if names is at top level
        if 'names' in checkpoint:
            checkpoint['names'] = new_names_dict
    
    print(f"\nUpdated class names:")
    for idx, name in new_names_dict.items():
        print(f"  {idx}: {name}")
    
    # Save the updated model
    output_path = Path(model_path).parent / f"{Path(model_path).stem}_fixed.pt"
    torch.save(checkpoint, output_path, _use_new_zipfile_serialization=False)
    
    print(f"\nSaved updated model to: {output_path}")
    print("You can rename this file to replace the original if needed.")

if __name__ == "__main__":
    # Define the correct class names as a list (in order)
    correct_names_list = [
        "s1",
        "m1",
        "t1",
        "f1",
        "ff1",
        "s2",
        "m2",
        "t2",
        "f2",
        "ff2",
        "s3",
        "m3",
        "t3",
        "f3",
        "ff3",
        "s4",
        "m4",
        "t4",
        "f4",
        "ff4",
        "s5",
        "m5",
        "t5",
        "s6",
        "m6",
        "t6",
        "s7",
        "m7",
        "t7",
        "s8",
        "m8",
        "t8",
        "s9",
        "m9",
        "t9",
        "east",
        "fa",
        "north",
        "zhong",
        "south",
        "bai",
        "west",
        "joker",
    ]
    
    # Convert list to dictionary (index -> name)
    correct_names = {i: name for i, name in enumerate(correct_names_list)}
    
    # Path to your model
    model_path = "IR_model/runs/detect/m_model_v3/weights/best.pt"
    
    print("=" * 60)
    print("YOLO Model Class Name Updater")
    print("=" * 60)
    
    # List of model directories to update
    model_dirs = ["m_model_v2"]
    
    # Update both best and last models for each directory
    for model_dir in model_dirs:
        print(f"\n\n{'='*60}")
        print(f"Processing {model_dir}")
        print('='*60)
        
        for model_file in ["best.pt", "last.pt"]:
            full_path = f"IR_model/runs/detect/{model_dir}/weights/{model_file}"
            print(f"\nProcessing {model_file}...")
            print("-" * 60)
            try:
                update_model_class_names(full_path, correct_names)
            except FileNotFoundError:
                print(f"File not found: {full_path} (skipping)")
            except Exception as e:
                print(f"Error processing {model_file}: {e}")
    
    print("\n" + "=" * 60)
    print("Done! All models updated.")
    print("=" * 60)

import os

# === CONFIGURATION ===
input_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\labels'  # Update this path
output_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\newlabels'  # Update this path

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Process each label file
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            for line in infile:
                line = line.strip()  # Remove leading and trailing whitespace
                if line:  # Skip empty lines
                    parts = line.split()
                    try:
                        # Convert the first part to an integer without rounding
                        class_id = int(float(parts[0]))
                        # Keep the remaining parts as they are
                        updated_line = ' '.join([str(class_id)] + parts[1:])
                        outfile.write(updated_line + '\n')
                    except (ValueError, IndexError):
                        print(f"Skipping invalid line in {filename}: {line}")

print("✅ Conversion complete. New labels saved in 'new_labels' folder.")

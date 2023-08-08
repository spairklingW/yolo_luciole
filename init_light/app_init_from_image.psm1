# Print current directory
Get-Location

# Activate virtual environment (assuming the virtual environment is in the current directory)
.\py311\Scripts\Activate

# Run Python script with parameters
python .\app_initializer.py `
    --input .\images\living_room.jpg `
    --output .\video\out_video.jpg `
    --mode image `
    --light_pos_file light_pos.yaml `
    --metadata metadata.yaml `
    --verbose $true `
    --config_path .\config-init.yaml

source ../py311/bin/activate

python app_initializer.py \
          --input ./video/one_light.mp4 \
          --output ./video/out_video.avi \
          --mode video \
          --light_pos_file light_pos.yaml \
          --metadata metadata.yaml \
          --verbose true \
          --config_path ./config-init.yaml

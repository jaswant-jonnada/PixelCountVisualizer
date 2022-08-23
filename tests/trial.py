from src.visualizer import visualizer
# from ../visualizer/visualizer import PixelCountVisualizer


def main():
    image_name = "data/hand.jpeg"
    # video_path = "/Users/jaswantjonnada/Documents/BP_anamoly_detection/data/AnomalyDetectionExps1/MPOPPCPH21790001/random_background_followed_by_finger_placement/video_snap_16512063555422022-04-29T04:26:03Z.mp4"

    video_path = "data/160330_5_Compass1_Mpeg4_4K.mov"
    pixel_visualizer = visualizer.PixelCountVisualizer(video_path)

    pixel_visualizer.run()

    image_pixel_visualizer = visualizer.PixelCountVisualizer(image_name)
    image_pixel_visualizer.run()


if __name__ == "__main__":
    main()

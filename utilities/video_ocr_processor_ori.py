import os
import cv2
import easyocr
import asyncio

class VideoProcessor:
    def __init__(self, video_paths, output_dir="instance/results"):
        self.video_paths = video_paths
        self.output_dir = output_dir
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.res_dic = list()

    async def _remove_duplicate_content(self, ocr_text_list):
        unique_results = []
        for ocr_text in ocr_text_list:
            ocr_text_no_punctuation = ocr_text.replace("。", "").replace(";", "").replace(",", "").replace(".", "")
            if ocr_text_no_punctuation not in unique_results:
                unique_results.append(ocr_text_no_punctuation)

        return unique_results

    async def _save_result(self, output_filepath, unique_results):
        with open(output_filepath, 'w') as file:
            for result in unique_results:
                file.write(f"{result}\n")

    async def process_videos(self):
        for video_name in self.video_paths:
            video_path = os.path.join("instance/video", video_name)
            output_filename = os.path.splitext(video_name)[0] + ".txt"
            output_filepath = os.path.join(self.output_dir, output_filename)

            try:
                video = cv2.VideoCapture(video_path)
                if not video.isOpened():
                    raise Exception(f"Error opening video file: {video_path}")

                frame_count = 0
                ocr_text_list = []
                while video.isOpened():
                    ret, frame = video.read()
                    if not ret:
                        break

                    frame_count += 1
                    if frame_count % 50 != 0:
                        continue

                    ocr_results = self.reader.readtext(frame)
                    ocr_text = ""

                    for (bbox, text, prob) in ocr_results:
                        ocr_text += text

                    print(f"{video_name} idx: {frame_count} Content: {ocr_text}")
                    if ocr_text not in ocr_text_list:
                        ocr_text_list.append(ocr_text)

                unique_results = await self._remove_duplicate_content(ocr_text_list)
                await self._save_result(output_filepath, unique_results)

                self.res_dic[video_name] = '\n'.join(unique_results)

                video.release()
                cv2.destroyAllWindows()

            except Exception as e:
                print(f"Error processing video {video_path}: {e}")


async def main():
    processor = VideoProcessor(video_paths)
    await processor.process_videos()


if __name__ == "__main__":
    video_paths = ["a.mp4"]  # List of video paths
    asyncio.run(main())

import os

import redis
import cv2
import easyocr
import asyncio


from enums import FileStatus, UpdateField

r = redis.Redis(host="127.0.0.1", port=6379)


class VideoProcessor:
    def __init__(self, video_paths, output_dir="instance/results"):
        self.video_paths = video_paths
        self.output_dir = output_dir
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.res_dic = dict()

    def _check_process_status(self, video_name):
        file_status = r.hgetall(video_name).get(UpdateField.STATUS.value.encode())
        if isinstance(file_status, bytes):
            file_status = file_status.decode()

        if file_status == FileStatus.COMPLETED.value:
            return True

    def _remove_duplicate_content(self, ocr_text_list):
        unique_results = []
        for ocr_text in ocr_text_list:
            ocr_text_no_punctuation = ocr_text.replace("。", "").replace(";", "").replace(",", "").replace(".", "")
            if ocr_text_no_punctuation not in unique_results:
                unique_results.append(ocr_text_no_punctuation)

        return unique_results

    def _update_file_status(self, file_name, key, value):

        if key.encode() in r.hgetall(file_name):
            r.hdel(file_name, key)

        r.hset(file_name, key, value)

    def _save_result(self, output_filepath, unique_results):
        with open(output_filepath, 'w') as file:
            for result in unique_results:
                file.write(f"{result}\n")

    def process_videos(self):
        for video_name in self.video_paths:
            if self._check_process_status(video_name):
                continue

            video_path = os.path.join("instance/video", video_name)
            output_filename = os.path.splitext(video_name)[0] + ".txt"
            output_filepath = os.path.join(self.output_dir, output_filename)

            video = cv2.VideoCapture(video_path)
            if not video.isOpened():
                self._update_file_status(video_name, UpdateField.STATUS.value, FileStatus.FAILED.value)
                raise Exception(f"Error opening video file: {video_path}")

            self._update_file_status(video_name, UpdateField.STATUS.value, FileStatus.PROCESSING.value)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            frame_count = 0
            ocr_text_list = []

            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break

                frame_count += 1
                if frame_count % 150 != 0:
                    continue

                self._update_file_status(video_name, UpdateField.PROGRESS.value, f"{frame_count}/{total_frames}")

                ocr_results = self.reader.readtext(frame)
                ocr_text = ""

                for (bbox, text, prob) in ocr_results:
                    ocr_text += text

                print(f"{video_name} idx: {frame_count} Content: {ocr_text}")
                if ocr_text not in ocr_text_list:
                    ocr_text_list.append(ocr_text)

            unique_results = self._remove_duplicate_content(ocr_text_list)

            format_result = '\n'.join(unique_results)
            self._save_result(output_filepath, format_result)
            self._update_file_status(video_name, UpdateField.RESULT.value, format_result)
            self._update_file_status(video_name, UpdateField.STATUS.value, FileStatus.COMPLETED.value)

            video.release()
            cv2.destroyAllWindows()

            # except Exception as e:
            #     print(f"Error processing video {video_path}: {e}")


async def main():
    processor = VideoProcessor(video_paths)
    await processor.process_videos()


if __name__ == "__main__":
    video_paths = ["a.mp4"]  # List of video paths
    asyncio.run(main())

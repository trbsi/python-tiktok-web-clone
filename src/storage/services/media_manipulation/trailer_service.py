import subprocess
import uuid

from app.utils import remote_file_path_for_media
from src.media.models import Media
from src.storage.services.remote_storage_service import RemoteStorageService


class TrailerService:
    """
    Generate a trailer by cutting evenly spaced clips from a video.

    :param input_file: Path to the input video file
    :param output_file: Path to the output trailer file
    :param clip_count: How many clips to extract
    :param min_length: Minimum trailer length in seconds
    :param max_length: Maximum trailer length in seconds
    :param percentage: Fraction of video duration to use for trailer
    """

    def make_trailer(
            self,
            media: Media,
            local_file_type: str,
            local_file_path: str,
            local_file_path_directory: str,
            clip_count=3,
            min_length=7,
            max_length=60,
            percentage=0.15
    ):

        remote_storage_service = RemoteStorageService()

        # Get video duration with ffprobe
        command = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            local_file_path
        ]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        duration = float(result.stdout.strip())

        # Cap-based trailer length
        target_length = duration * percentage
        trailer_length = max(min_length, min(max_length, target_length))

        # Length of each clip
        clip_length = trailer_length / clip_count

        # Pick positions evenly spaced across the video
        positions = [duration * (i + 1) / (clip_count + 1) for i in range(clip_count)]

        parts = []
        part_uuid = uuid.uuid4()
        for i, pos in enumerate(positions):
            start = max(pos - clip_length / 2, 0)
            part = f"{local_file_path_directory}/{part_uuid}_part_{i}.mp4"
            command = [
                "ffmpeg", "-y", "-ss", str(start), "-i", str(local_file_path),
                "-t", str(clip_length), "-c:v", "libx264", "-c:a", "aac",
                str(part)
            ]
            subprocess.run(command, check=True)
            parts.append(part)

        # Merge into final trailer
        cmd = ["ffmpeg", "-y"]

        # Add each part as an input
        for part in parts:
            cmd += ["-i", part]

        # Build the filter_complex string
        filter_parts = []
        for i in range(len(parts)):
            filter_parts.append(f"[{i}:v][{i}:a]")
        filter_complex = "".join(filter_parts) + f"concat=n={len(parts)}:v=1:a=1[outv][outa]"

        # Complete FFmpeg command
        output_trailer_file_path = f'{local_file_path_directory}/{uuid.uuid4()}.mp4'
        cmd += ["-filter_complex", filter_complex, "-map", "[outv]", "-map", "[outa]", str(output_trailer_file_path)]

        subprocess.run(command, check=True)

        # upload to remote
        remote_file_name = f'{media.__class__.__name__}_{media.id}_trailer_{uuid.uuid4()}.mp4'
        remote_file_path = remote_file_path_for_media(media, remote_file_name)

        file_info = remote_storage_service.upload_file(
            local_file_type=local_file_type,
            local_file_path=output_trailer_file_path,
            remote_file_path=remote_file_path,
        )

        media.file_trailer = file_info
        media.save()

        return {
            'parts': parts,
            'output_trailer_file_path': output_trailer_file_path
        }

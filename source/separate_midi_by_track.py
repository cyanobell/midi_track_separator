import os

from mido import MidiFile, MidiTrack


def separate_midi_by_track(midi: MidiFile):
    separated_midi_list = []
    filename_without_extension, extension = os.path.splitext(midi.filename)
    if len(midi.tracks) <= 1:
        # トラック数が1つ以下の場合は、目的を満たしているので作成しない。
        return []

    for i, track in enumerate(midi.tracks):
        track_name = track.name if track.name else f"track{i}"
        sanitized_name = track_name.replace(" ", "_")

        output_filename = f"{filename_without_extension}-{sanitized_name}{extension}"

        new_midi = MidiFile(
            type=midi.type,
            filename=output_filename,
            charset=midi.charset,
            debug=midi.debug,
            clip=midi.clip,
            ticks_per_beat=midi.ticks_per_beat,
            tracks=[track],
        )
        separated_midi_list.append(new_midi)

    return separated_midi_list


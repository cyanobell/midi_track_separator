import argparse
import os
import shutil
from fileinput import filename

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

from source.separate_midi_by_track import separate_midi_by_track
SOURCE_DIR_NAME = "source_midi_file"




def handle_file(input_path, hide_source=False):
    midi = MidiFile(input_path)

    separated_midi_list = separate_midi_by_track(midi)
    if not separated_midi_list:
        print(f"Skipped: {midi.filename}")
        return

    for separated_midi in separate_midi_by_track(midi):
        separated_midi.save(filename=separated_midi.filename)
        print(f"Saved: {separated_midi.filename}")

    if hide_source:
        # source ディレクトリを作って移動
        source_dir = os.path.join(os.path.dirname(input_path), SOURCE_DIR_NAME)
        os.makedirs(source_dir, exist_ok=True)

        new_path = os.path.join(source_dir, os.path.basename(input_path))

        if os.path.exists(new_path):
            print(f"Warning: {new_path} already exists. Overwriting.")

        shutil.move(input_path, new_path)
        print(f"Moved original MIDI to: {new_path}")


def main():
    parser = argparse.ArgumentParser(description="Separate MIDI file by track.")
    parser.add_argument("-i", "--input", required=True, help="Path to input MIDI file. or Directory")
    parser.add_argument(
        "--hide_source_midi",
        action="store_true",
        help="Move original MIDI files to 'source_midi_file/' subdirectory after processing."
    )

    args = parser.parse_args()

    input_path = args.input
    hide_source_midi = args.hide_source_midi

    if os.path.isfile(input_path):
        handle_file(input_path, hide_source_midi)
    elif os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            dirs[:] = [d for d in dirs if d != SOURCE_DIR_NAME]
            for file in files:
                if file.lower().endswith(".mid"):
                    full_path = os.path.join(root, file)
                    handle_file(full_path, hide_source_midi)

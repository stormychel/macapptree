import AppKit
import macapptree.apps as apps
from macapptree.uielement import UIElement
from macapptree.extractor import extract_window
from macapptree.screenshot_app_window import screenshot_window_to_file
from macapptree.window import segment_window_components
import argparse
import json


def main(app_bundle, perform_hit_test, output_accessibility_file, output_screenshot_file):
    workspace = AppKit.NSWorkspace.sharedWorkspace()
    app = apps.application_for_bundle(app_bundle, workspace)
    app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
    application = apps.application_for_process_id(app.processIdentifier())

    window = apps.windows_for_application(application)[-1]
    window_element = UIElement(window)

    extracted = extract_window(
            window_element, app_bundle, output_accessibility_file, perform_hit_test, False
        )
    
    if not extracted:
        raise "Couldn't extract accessibility"
    
    if output_screenshot_file:
        output_croped, _ = screenshot_window_to_file(app.localizedName(), window_element.name, output_screenshot_file)
        output_segmented = segment_window_components(window_element, output_croped)

        print(json.dumps({
            "croped_screenshot_path": output_croped,
            "segmented_screenshot_path": output_segmented
        }))
        

# main function
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-a", type=str, required=True, help="The application bundle identifier")
    arg_parser.add_argument("--oa", type=str, required=True, help="Accessibility output file")
    arg_parser.add_argument("--os", type=str, default=None, required=False, help="Screenshot output file")
    arg_parser.add_argument("--hit-test", action="store_true", help="Perform hit test")

    args = arg_parser.parse_args()
    app_bundle = args.a
    output_accessibility_file = args.oa
    output_screenshot_file = args.os
    perform_hit_test = args.hit_test

    # start processing all the running applications or the specified application
    main(app_bundle, perform_hit_test, output_accessibility_file, output_screenshot_file)

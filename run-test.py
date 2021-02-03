# Setup:
#
# Change "Exposure, Auto" to "Manual Mode"
# (Default value: 3)
# $ v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1
# To confirm:
# $ v4l2-ctl -d /dev/video2 --get-ctrl=exposure_auto
# exposure_auto: 1

import time
import datetime
import argparse
import robot
import vision
import importlib

def parse_arguments():
    parser = argparse.ArgumentParser(description='Tapster Robot - App Launch Test')

    parser.add_argument('-p', '--port', action='store', dest='port',
        required=True,
        help='Serial port of robot')

    parser.add_argument('-c', '--camera', action='store', dest='camera',
        required=True,
        type=int,
        help='Integer index of camera capture device')

    parser.add_argument('-n', '--name', action='store', dest='name',
        default = "iphone_6s",
        help='Phone module name: (e.g. iphone_6s, iphone_xs_max) Default: iphone_6s')

    parser.add_argument('-i', '--iterations', action='store', dest='iterations',
        default=1,
        type=int,
        help='Integer number of test iterations to run. Default: 1')

    parser.add_argument('-t', '--type', action='store', dest='type',
        default = "warm",
        help='Launch type: {warm, cold} Default: warm')

    parser.add_argument('-r', '--results', action='store', dest='results',
        default="results",
        help='Name of directory to store results data. Default: results')

    parser.add_argument('--save', action='store_true', dest='save',
        default = False,
        help='Save test data in RESULTS directory. Will only save results if this flag is set.')

    arguments = parser.parse_args()
    return arguments

if __name__ == '__main__':
    args = parse_arguments()

    #Initialize
    robot = robot.Robot(args.port)
    camera = vision.Vision(args.camera)
    # Dynamically import the phone module based on the --name command line flag
    phone_module = importlib.import_module(args.name)
    phone = phone_module.Phone(robot)

    print("-------------------")
    print("Tapster - App Launch Test")
    print("-------------------")
    print()
    print("  Phone name: " + args.name)
    print("  Launch type: " + args.type)
    print("  Number of iterations: " + str(args.iterations))
    print("  Save results: " + str(args.save))
    if args.results:
        print("  Results directory: " + args.results)
    print()

    if args.save:
        file_timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        # Open results file
        results = open(args.results + "/" + phone.name + "--" + args.type +  "-start--" + file_timestamp + ".txt", "w")
        results.write("Iteration, Duration\n")

    phone.go_to_start_position()

    # Start main timer
    main_timer_start = time.perf_counter()

    for i in range(args.iterations):
        print(f"Iteration #{i+1}")
        camera.clear_image_buffer()
        phone.open_app()
        camera.look_for_image()
        elapsed_time = camera.timestamp - phone.start_timestamp
        print("  Elapsed time:", elapsed_time)

        if args.save:
            results.write(f"{i+1}, {elapsed_time}\n")

        time.sleep(0.5)

        if args.type == "warm":
            print("  Closing app\n")
            phone.close_app()
        else:
            print("  Quitting app\n")
            phone.quit_app()

    # Stop main timer
    main_timer_stop = time.perf_counter()
    main_timer_duration = main_timer_stop - main_timer_start
    print("Total time:", str(datetime.timedelta(seconds=main_timer_duration)))

    # Close results file
    if args.save:
        results.close()

    # When done, return to starting position
    phone.go_to_start_position()
    camera.clean_up()
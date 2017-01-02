#!/usr/bin/env python

import sys
import argparse
import os
import yaml

# Global variables
prog = os.path.basename(
    __file__
)
prog_dir = ".snk"
test_prefix = "test__"


def main(
):
    # Top level parser
    parser = argparse.ArgumentParser(
    )
    parser.add_argument(
        "-d",
        "--directory",
        metavar="DIR",
        help="directory to save program files",
        default=prog_dir
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show additional output"
    )
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands'
    )

    # Parser for init
    parser_init = subparsers.add_parser(
        "init",
        help="initializes the current directory"
    )
    parser_init.set_defaults(
        func=init
    )

    # Parser for add
    parser_add = subparsers.add_parser(
        "add",
        help="adds test files and processes them"
    )
    parser_add.add_argument(
        "tests",
        metavar="FILE",
        help="test file to add and process",
        nargs='+'
    )
    parser_add.set_defaults(
        func=add
    )

    # Parser for commit
    parser_commit = subparsers.add_parser(
        "commit",
        help="adds sneak peek file and processes it"
    )
    parser_commit.add_argument(
        "sneak_peek",
        metavar="FILE",
        help="sneak peek file to compare to tests"
    )
    parser_commit.set_defaults(
        func=commit
    )

    # Main
    args = parser.parse_args(
    )
    if args.verbose:
        print "%s ran with verbose output" % prog

    args.directory = os.path.abspath(
        args.
        directory
    )
    if args.verbose:
        print "%s directory: %s" % (
            prog,
            args.
            directory
        )
    args.func(
        args
    )


#
def assert_directory(
        directory
):
    if not os.path.isdir(
            directory
    ):
        sys.exit(
            "fatal: not a directory: %s"
            %
            (prog,
             directory
             )
        )


#
def init(
        args
):
    if os.path.isdir(
            args.
            directory
    ):
        exit(
            "Existing %s directory: %s"
            %
            (prog,
             args.
             directory
             )
        )

        os.makedirs(
            args.
            directory
        )
        print "Initialized empty %s directory: %s" % (
            prog,
            args.
            directory
        )


        #
def add(
        args
):
    assert_directory(
        args.
        directory
    )
    for test in args.tests:
        # TODO: Handle UNIX file expressions, wildcards, etc
        test_infile = os.path.abspath(
            test
        )
        test_name = os.path.basename(
            test_infile
        )
        test_object = None
        test_outfile = args.directory + "/" + test_name + ".yaml"
        if not os.path.isfile(
                test_infile
        ):
            print "warning: test %s cannot be found, ignoring: %s" % (
                test_name,
                test_infile
            )
        elif os.path.exists(
                test_outfile
        ):
            print "warning: test %s is already added, ignoring: %s" % (
                test_name,
                test_outfile
            )
        else:
            print "%s is a valid file: %s -> %s" % (
                test,
                test_infile,
                test_outfile
            )
            test_infile_object = open(
                test_infile,
                "r"
            )
            test_outfile_object = open(
                test_outfile,
                "w"
            )
            test_object = dict(
                name=test_name,
                path=test_infile,
                text=map(
                    str.
                    rstrip,
                    test_infile_object
                )
            )
            test_outfile_object.write(
                yaml.
                dump(
                    test_object
                )
            )
            test_infile_object.close(
            )
            test_outfile_object.close(
            )


#
def commit(
        args
):
    assert_directory(
        args.
        directory
    )


#
if __name__ == "__main__":
    main(
    )

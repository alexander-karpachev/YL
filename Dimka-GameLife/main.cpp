#include <cstdio>
#include <fstream>
#include <iostream>
#include <regex>
#include <stdexcept>
#include <string>
#include <thread>
#include "./lib/include/game_interface.hpp"

#define default "./examples/glaider.txt"

using namespace std;

void redisplay(Universe* uni);

int main(int argc, char* argv[]) {
    std::cout << "\033[2J\033[H";

    std::regex files_pattern(R"(^(.+)=(.+)$)");
    std::regex iters_pattern(R"(^(.+)=(\d+)$)");
    std::smatch matches;

    str input_name = default;
    bool is_input = false;
    str output_name;
    bool is_output = false;
    int iterations;
    bool is_iterations = false;
    Universe* uni = nullptr;

    if (argc < 2) {
        input_name = default;
    }
    else if (argc == 2) {
        str arg = argv[1];
        if (arg == "-h" || arg == "--help") {
            std::ifstream help_args("./lib/args_help.txt");
            if (!help_args.is_open()) {
                cerr << "\033[1;91m" << "CRITICAL ERROR: help file is damaged or not flound! You need to reload it from github repository!\n\033[0;0m";
                return 1;
            }
            else {
                str line;
                while (std::getline(help_args, line)) {
                    cout << line << "\n";
                }
                return 0;
            }
        }
        if (std::regex_match(arg, matches, files_pattern)) {
            if (matches[1] == "-s" || matches[1] == "--source") input_name = matches[2];
            else cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "Wrong argument!\n\t| at \033[0;0m" << arg << "\n\033[0;91mSee output of --help command.\n\033[0;0m";
        }
        else input_name = arg;
    }
    else if (argc > 4) {
        cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "A lot of arguments! See output of --help comand.\n\033[0;0m";
        input_name = default;
    }
    else {
        bool err_flag = false;
        for (int i = 1; i < argc; i++) {
            str arg = argv[i];
            if (std::regex_match(arg, matches, iters_pattern))  {
                if (matches[1] == "-i" || matches[1] == "--iterations") {
                    if (is_iterations) {
                        cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "This argument is already specified!\n\t| at \033[0;0m" << arg << "\n";
                        cerr << "\033[0;91mSee output of --help command.\n\033[0;0m";
                        err_flag = true;
                        break;
                    }
                    else {
                        iterations = std::stoi(matches[2]);
                        is_iterations = true;
                    }
                }
                else {
                    cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "Unknown argument at: \033[0;0m" << arg << "\n";
                    err_flag = true;
                    break;
                }
            }
            else if (std::regex_match(arg, matches, files_pattern)) {
                if (matches[1] == "-s" || matches[1] == "--source") {
                    if (is_input) {
                        cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "This argument is already specified!\n\t| at \033[0;0m" << arg << "\n";
                        cerr << "\033[0;91mSee output of --help command.\n\033[0;0m";
                        err_flag = true;
                        break;
                    } 
                    else {
                        input_name = matches[2];
                        is_input = true;
                    }
                }
                else if (matches[1] == "-o" || matches[1] == "--output") {
                    if (is_output) {
                        cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "This argument is already specified!\n\t| at \033[0;0m" << arg << "\n";
                        cerr << "\033[0;91mSee output of --help command.\n\033[0;0m";
                        err_flag = true;
                        break;
                    } 
                    else {
                        output_name = matches[2];
                        is_output = true;
                    }
                }
                else {
                    cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "Unknown argument at: \033[0;0m" << arg << "\n";
                    err_flag = true;
                    break;
                }
            }
            else {
                cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "Unknown argument at: \033[0;0m" << arg << "\n";
                err_flag = true;
                break;
            }
        }

        if (!is_input || !is_output || !is_iterations) {
            cerr << "\033[1;91m" << "ERROR: " << "\033[0;91m" << "Some arguments wasn't specified!\n";
            if (!is_input) cerr << "\t| input file name wasn't secified\n";
            if (!is_output) cerr << "\t| output file name wasn't secified\n";
            if (!is_iterations) cerr << "\t| iterations count wasn't secified or iterations count less then zero\n";
            cerr << "\033[0;0m";
            input_name = default;
        }
        else {
            if (err_flag) {
                input_name = default;
            }
            else {
                cout << "Reading a file \"" << input_name << "\"...\n";

                bool not_error = true;
                try {
                    uni = read_universe(input_name);
                }
                catch (std::invalid_argument err) {
                    cerr << "\033[1;91m" << "ERROR: " << err.what();
                    not_error = false;
                }
                if (not_error) {
                    cout << "Reading done.\n";

                    for (int i = 0; i < iterations; i++) {
                        cout << "\rProgress: " << (int)((i + 1) / (double)iterations * 100) << "%";
                        if (uni->tick()) {
                            cout << "\n";
                            cout << "\033[0;93mThe field has reached a static position, the operation is interrupted.\033[0;0m";
                            break;
                        }
                    }
                    cout << "\nOperation done.\nWriting in file \"" << output_name << "\"...\n";
                    write_universe(*uni, output_name);
                    cout << "Succefully written.\n";

                    return 0;
                }
                else {
                    input_name = default;
                }
            }
        }
    }

    try {
        uni = read_universe(input_name);
    }
    catch (std::invalid_argument err) {
        if (input_name != default) {
            cerr << "\033[1;91m" << "ERROR: " << err.what() << "\n";
            uni = read_universe(default);
        }
        else {
            cerr << "\033[1;91m" << "ERROR: " << err.what() << "\n";
            cerr << "\033[1;91m" << "CRITICAL ERROR: default file is damaged or not flound! You need to fix it or reload from github repository!\n\033[0;0m";
            return 1;
        }
    }

    cout << "\033[0;0m";
    if (input_name == default) {
        cout << "\033[0;96mDefault file will be opened.\n\033[0;0m";
    }

    cout << "Name of universe: " << "\033[1;0m" << uni->get_name() << "\033[0;0m\n";
    cout << "Rule: B";
    int_set t = uni->get_birth(); 
    for (auto it = t.begin(); it != t.end(); it++) {
        cout << *it;
    }
    cout << "/S";
    t = uni->get_survival();
    for (auto it = t.begin(); it != t.end(); it++) {
        cout << *it;
    }
    cout << "\n";
    cout << "Size: width=" << uni->get_field().get_width() << " height=" << uni->get_field().get_height() << "\n";
    cout << "Iteration: " << uni->get_ticks() << "\n";
    cout << uni->get_field();

    str cmd;
    std::regex dump_pattern(R"(^dump\s+<(.+)>$)");
    std::regex tick_pattern(R"(^tick(\s+<n=(\d+)(\s+t=(\d+))?>)?$)");
    while (1) {
        cout << "command> ";
        std::getline(std::cin, cmd);

        if (cmd == "exit") {
            break;
        }
        else if (cmd == "help") {
            std::ifstream help_args("./lib/help.txt");
            if (!help_args.is_open()) {
                cerr << "\033[1;91m" << "CRITICAL ERROR: help file is damaged or not flound! You need to reload it from github repository!\n\033[0;0m";
                return 1;
            }
            else {
                std::cout << "\033[2J\033[H";
                str line;
                while (std::getline(help_args, line)) {
                    cout << line << "\n";
                }
            }
        }
        else {
            if (std::regex_match(cmd, matches, dump_pattern)) {
                try {
                    try {
                        write_universe(*uni, matches[1]);
                    }
                    catch (std::invalid_argument err) {
                        cerr << "\033[1;91m" << "ERROR: " << err.what() << "\n";
                    }
                }
                catch (std::invalid_argument err) {}
            }
            else if (std::regex_match(cmd, matches, tick_pattern)) {
                if (matches.size() > 1 && matches[1].matched) {
                    int n = 1;
                    int t = 0;
                    if (matches.size() > 2 && matches[2].matched) {
                        n = stoi(matches[2]);
                    }
                    if (matches.size() > 4 && matches[4].matched) {
                        t = stoi(matches[4]);
                    }
                    if (n > 1) {
                        bool break_flag = false;
                        for (int i = 0; i < n; i++) {
                            if (t > 0) {
                                std::this_thread::sleep_for(std::chrono::milliseconds(t));
                            }
                            if (uni->tick()) {
                                break_flag = true;
                                redisplay(uni);
                                cout << "\033[0;93mThe field has reached a static position, the operation is interrupted.\n\033[0;0m";
                                break;
                            }
                            if (t > 0) {
                                cout << "\033[" << uni->get_field().get_height() + 2 << "A\r";
                                cout << "Iteration: " << uni->get_ticks() << "\n";
                                cout << uni->get_field() << "\n";
                            }
                        }
                        if (t == 0 && !break_flag) {
                            redisplay(uni);
                        }
                    }
                    else if (n == 0) {
                        redisplay(uni);
                    }
                    else {
                        redisplay(uni);
                        if (uni->tick()) {
                            cout << "\033[0;93mThe field has reached a static position.\n\033[0;0m";
                        }
                    }
                }
                else {
                    redisplay(uni);
                    if (uni->tick()) {
                        cout << "\033[0;93mThe field has reached a static position.\n\033[0;0m";
                    }
                }

            }
            else {
                redisplay(uni);
                cerr << "\033[1;91m" << "ERROR: \033[0;91m" << "Unknown command! \033[0;0m" << "\n";
            }
        }
    }

    return 0;
}

void redisplay(Universe* uni) {
    std::cout << "\033[2J\033[H";
    cout << "Name of universe: " << "\033[1;0m" << uni->get_name() << "\033[0;0m\n";
    cout << "Rule: B";
    int_set t = uni->get_birth(); 
    for (auto it = t.begin(); it != t.end(); it++) {
        cout << *it;
    }
    cout << "/S";
    t = uni->get_survival();
    for (auto it = t.begin(); it != t.end(); it++) {
        cout << *it;
    }
    cout << "\n";
    cout << "Size: width=" << uni->get_field().get_width() << " height=" << uni->get_field().get_height() << "\n";
    cout << "Iteration: " << uni->get_ticks() << "\n";
    cout << uni->get_field();
}

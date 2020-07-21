#include <iostream>
using namespace std;

int main() {
    string str;
    cout << "Enter password:";
    getchar();
    cout << "Welcome to the MySQL monitor.  Commands end with ; or \\g." << endl;
    cout << "Your MySQL connection id is 15" << endl;
    cout << "Server version: 8.0.16 Homebrew" << endl;
    cout << endl;
    cout << "Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved." << endl;
    cout << endl;
    cout << "Oracle is a registered trademark of Oracle Corporation and/or its" << endl;
    cout << "affiliates. Other names may be trademarks of their respective" << endl;
    cout << "owners." << endl;
    cout << endl;
    cout << "Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement." << endl;
    cout << endl;
    cout << "mysql> ";
    getline(cin, str);
    cout << "Database changed" << endl;
    cout << "mysql> ";
    getline(cin, str);
    cout << "+------------------+" << endl;
    cout << "| Tables_in_facedb |" << endl;
    cout << "+------------------+" << endl;
    cout << "| check_log        |" << endl;
    cout << "| login_face       |" << endl;
    cout << "+------------------+" << endl;
    cout << "2 rows in set (0.01 sec)" << endl;
    cout << endl;
    cout << "mysql> ";
    getline(cin, str);
    cout << "+----------+" << endl;
    cout << "| count(*) |" << endl;
    cout << "+----------+" << endl;
    cout << "|  1000000 |" << endl;
    cout << "+----------+" << endl;
    cout << "1 row in set (0.00 sec)" << endl;
    cout << endl;
    cout << "mysql> ";
    getline(cin, str);
    cout << "Bye" << endl;
}

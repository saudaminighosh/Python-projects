// Save as food_ordering.cpp
#include <bits/stdc++.h>
using namespace std;

struct User {
    int id;
    string name;
    string email;
    string phone;
    string address;
};

struct MenuItem {
    int id;
    string name;
    string description;
    double price;
    string category;
};

struct OrderItem {
    int itemId;
    int qty;
    double price;
};

struct Order {
    int orderId;
    int userId;
    string orderDate;
    string status;
    double total;
    vector<OrderItem> items;
};

// --- Simple CSV helpers ---
vector<string> split(const string &s, char delim) {
    vector<string> out;
    string cur;
    stringstream ss(s);
    while (getline(ss, cur, delim)) out.push_back(cur);
    return out;
}

string trim(const string &s) {
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a==string::npos) return "";
    size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b-a+1);
}

// --- Persistence filenames ---
const string USERS_FILE = "users.csv";
const string MENU_FILE  = "menu.csv";
const string ORDERS_FILE = "orders.csv";

// --- Load / Save functions ---
vector<User> loadUsers() {
    vector<User> users;
    ifstream f(USERS_FILE);
    string line;
    while (getline(f, line)) {
        line = trim(line);
        if (line.empty()) continue;

        auto parts = split(line, ',');
        if (parts.size() < 4) continue;

        try {
            User u;
            u.id = stoi(trim(parts[0]));
            u.name = trim(parts[1]);
            u.email = trim(parts[2]);
            u.phone = trim(parts[3]);
            u.address = parts.size() > 4 ? trim(parts[4]) : "";
            users.push_back(u);
        } catch (const exception &e) {
            cerr << "Skipping invalid user line: " << line << endl;
            continue;
        }
    }
    return users;
}

void saveUser(const User &u) {
    ofstream f(USERS_FILE, ios::app);
    f << u.id << "," << u.name << "," << u.email << "," << u.phone << "," << u.address << "\n"<< flush;
}

vector<MenuItem> loadMenu() {
    vector<MenuItem> menu;
    ifstream f(MENU_FILE);
    string line;
    while (getline(f, line)) {
        line = trim(line);
        if (line.empty()) continue;

        auto parts = split(line, ',');
        if (parts.size() < 4) continue;

        try {
            MenuItem m;
            m.id = stoi(trim(parts[0]));
            m.name = trim(parts[1]);
            m.description = trim(parts[2]);
            m.price = stod(trim(parts[3]));  // SAFE conversion
            m.category = parts.size() > 4 ? trim(parts[4]) : "";
            menu.push_back(m);
        } catch (const exception &e) {
            cerr << "Skipping invalid menu line: " << line << endl;
            continue;
        }
    }
    return menu;
}

void saveOrder(const Order &o) {
    ofstream f(ORDERS_FILE, ios::app);
    stringstream itemsSs;
    for (size_t i=0;i<o.items.size();++i) {
        if (i) itemsSs << "<< flush;"<< flush;
        itemsSs << o.items[i].itemId << ":" << o.items[i].qty << ":" << o.items[i].price;
    }
    f << o.orderId << "," << o.userId << "," << o.orderDate << "," << o.status << "," 
      << fixed << setprecision(2) << o.total << "," << itemsSs.str() << "\n"<< flush;
}

// --- Helpers ---
int nextIdForFile(const string &fname) {
    ifstream f(fname);
    string line;
    int maxId = 0;
    while (getline(f, line)) {
        line = trim(line);
        if (line.empty()) continue;
        auto parts = split(line, ',');
        if (!parts.empty()) {
            try {
                int id = stoi(trim(parts[0]));
                if (id > maxId) maxId = id;
            } catch (...) { continue; }
        }
    }
    return maxId + 1;
}

string nowStr() {
    time_t t = time(nullptr);
    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&t));
    return string(buf);
}

// --- App ---
int main() {
    ios::sync_with_stdio(false);  // first thing
    cin.tie(nullptr);
    
    // Ensure files exist
    { ofstream f1(USERS_FILE, ios::app); ofstream f2(MENU_FILE, ios::app); ofstream f3(ORDERS_FILE, ios::app); }

    vector<User> users = loadUsers();
    cout << "Loading menu...\n"<< flush;
    vector<MenuItem> menu = loadMenu();
    cout << "Menu loaded.\n"<< flush;

    // Seed menu if empty
    if (menu.empty()) {
        menu = {
            {1, "Margherita Pizza", "Classic cheese & tomato", 8.99, "Pizza"},
            {2, "Veg Burger", "Patty, lettuce, tomato", 5.49, "Burger"},
            {3, "Caesar Salad", "Romaine, dressing, croutons", 6.50, "Salad"},
            {4, "French Fries", "Crispy fried potatoes", 2.99, "Sides"}
        };
        for (auto &m: menu) {
            ofstream f(MENU_FILE, ios::app);
            f << m.id << "," << m.name << "," << m.description << "," 
              << fixed << setprecision(2) << m.price << "," << m.category << "\n"<< flush;
        }
    }

    cout << "=== Food Ordering System (Console) ===\n"<< flush;

    User currentUser;
    bool loggedIn = false;

    while (true) {
        if (!loggedIn) {
            cout << "\n1) Register\n2) Login\n3) Exit\nChoose: "<< flush;
            int c; if(!(cin>>c)){cin.clear();cin.ignore(10000,'\n'); continue;}
            if (c==1) {
                User u;
                u.id = nextIdForFile(USERS_FILE);
                cout << "Name: "<< flush; cin.ignore(); getline(cin, u.name);
                cout << "Email: "<< flush; getline(cin, u.email);
                cout << "Phone: "<< flush; getline(cin, u.phone);
                cout << "Address: "<< flush; getline(cin, u.address);
                saveUser(u);
                users.push_back(u);
                cout << "Registered. Your user id: " << u.id << "\n"<< flush;
            } else if (c==2) {
                cout << "Enter email: "<< flush; string em; cin >> em;
                auto it = find_if(users.begin(), users.end(), [&](const User &x){ return x.email==em; });
                if (it != users.end()) {
                    currentUser = *it;
                    loggedIn = true;
                    cout << "Welcome back, " << currentUser.name << "!\n"<< flush;
                } else cout << "No user found. Please register.\n"<< flush;
            } else break;
        } else {
            cout << "\n1) View Menu\n2) View Cart & Place Order\n3) Order History (file)\n4) Logout\nChoose: "<< flush;
            int c; if(!(cin>>c)){cin.clear();cin.ignore(10000,'\n'); continue;}
            if (c==1) {
                cout << "\n--- Menu ---\n"<< flush;
                for (auto &m: menu) {
                    cout << m.id << ". " << m.name << " - $" << fixed << setprecision(2) << m.price 
                         << " (" << m.category << ")\n    " << m.description << "\n"<< flush;
                }
                cout << "Add item to cart? (y/n): "<< flush;
                char ch; cin >> ch;
                if (ch=='y' || ch=='Y') {
                    vector<OrderItem> cart;
                    while (true) {
                        cout << "Enter item id (0 to stop): "<< flush;
                        int id; cin >> id;
                        if (id==0) break;
                        auto it = find_if(menu.begin(), menu.end(), [&](const MenuItem &mi){ return mi.id==id;});
                        if (it==menu.end()) { cout << "Invalid id\n"<< flush; continue;}
                        cout << "Quantity: "<< flush; int q; cin >> q;
                        cart.push_back({id, q, it->price});
                    }
                    if (!cart.empty()) {
                        Order o;
                        o.orderId = nextIdForFile(ORDERS_FILE);
                        o.userId = currentUser.id;
                        o.orderDate = nowStr();
                        o.status = "Pending";
                        o.total = 0.0;
                        o.items = cart;
                        for (auto &it: cart) o.total += (it.price * it.qty);
                        saveOrder(o);
                        cout << "Order placed (id=" << o.orderId << "). Total: $" 
                             << fixed << setprecision(2) << o.total << "\n"<< flush;
                    } else cout << "No items added.\n"<< flush;
                }
            } else if (c==2) {
                vector<OrderItem> cart;
                while (true) {
                    cout << "Enter item id to add to cart (0 to stop): "<< flush;
                    int id; cin >> id;
                    if (id==0) break;
                    auto it = find_if(menu.begin(), menu.end(), [&](const MenuItem &mi){ return mi.id==id;});
                    if (it==menu.end()) { cout << "Invalid id\n"<< flush; continue;}
                    cout << "Quantity: "<< flush; int q; cin >> q;
                    cart.push_back({id, q, it->price});
                }
                if (!cart.empty()) {
                    Order o;
                    o.orderId = nextIdForFile(ORDERS_FILE);
                    o.userId = currentUser.id;
                    o.orderDate = nowStr();
                    o.status = "Pending";
                    o.total = 0.0;
                    o.items = cart;
                    for (auto &it: cart) o.total += (it.price * it.qty);
                    saveOrder(o);
                    cout << "Order placed (id=" << o.orderId << "). Total: $" 
                         << fixed << setprecision(2) << o.total << "\n"<< flush;
                } else cout << "Cart empty.\n"<< flush;
            } else if (c==3) {
                cout << "\n--- Your Orders ---\n"<< flush;
                ifstream f(ORDERS_FILE);
                string line;
                while (getline(f,line)) {
                    line = trim(line);
                    if (line.empty()) continue;
                    auto parts = split(line, ',');
                    if (parts.size() < 6) continue;
                    int oid = 0, uid = 0;
                    try {
                        oid = stoi(trim(parts[0]));
                        uid = stoi(trim(parts[1]));
                    } catch (...) { continue; }
                    if (uid != currentUser.id) continue;
                    string date = parts[2];
                    string status = parts[3];
                    string total = parts[4];
                    string itemsStr = parts[5];
                    cout << "Order #" << oid << " | " << date << " | " << status << " | $" << total << "\n"<< flush;

                    auto its = split(itemsStr, ';');
                    for (auto &it: its) {
                        if (trim(it).empty()) continue;
                        auto p = split(it, ':');
                        if (p.size() < 3) continue;
                        int mid = 0, qty = 0; double price = 0;
                        try {
                            mid = stoi(trim(p[0]));
                            qty = stoi(trim(p[1]));
                            price = stod(trim(p[2]));
                        } catch (...) { continue; }
                        auto mm = find_if(menu.begin(), menu.end(), [&](const MenuItem &m){ return m.id==mid;});
                        string mname = mm!=menu.end() ? mm->name : ("Item#" + to_string(mid));
                        cout << "   - " << mname << " x" << qty << " @ $" << fixed << setprecision(2) << price << "\n"<< flush;
                    }
                }
            } else if (c==4) {
                loggedIn = false;
                cout << "Logged out.\n"<< flush;
            } else {
                cout << "Unknown option.\n"<< flush;
            }
        }
    }

    cout << "Goodbye!\n"<< flush;
    return 0;
}
#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <cmath>
#include <cfloat>
#include <random>
#include <windows.h>

// animation
#include <chrono>
#include <thread>

using namespace std;

double gravity = 0.1;

enum Color {
    RESET = 0,
    RED = 31,
    GREEN = 32,
    YELLOW = 33,
    BLUE = 34
};

void setConsoleColor(Color color) {
    std::cout << "\033[" << color << "m";
}

void resetConsoleColor() {
    std::cout << "\033[0m";
}

class Element {
    protected:
        double x,y,dx = 0,dy = 0,ax = 0,ay = gravity;
        Color color;
        vector<char> charMap = {'@', '#', '8', '&', 'o', ':', '*', '.', '`'}; // from lightest to darkest
    
    public:
        Element() {}
        Element(int x, int y) {
            this->x = x;
            this->y = y;
        }
        Element(int x, int y,Color color) {
            this->x = x;
            this->y = y;
            this->color = color;
        }
        virtual ~Element() {}

        // methods

        void update() {
            this->x += this->dx;
            this->y += this->dy;
            this->dx += this->ax;
            this->dy += this->ay;
        }

        pair<double,double> getPos() {
            return {x,y};
        }

        pair<double,double> getVelocity() {
            return {dx,dy};
        }

        pair<double,double> getAcceleration() {
            return {ax,ay};
        }

        void setPosition(double x, double y) {
            this->x = x;
            this->y = y;
        }

        void setVelocity(double dx, double dy) {
            this->dx = dx;
            this->dy = dy;
        }

        void setAcceleration(double ax, double ay) {
            this->ax = ax;
            this->ay = ay;
        }

        Color getColor() {
            return color;
        }

        vector<char> getCharMap() {
            return charMap;
        }
};

class Sphere: public Element {
    protected:
        double r,lx = 5, ly = 5;
    public:
        Sphere() {}
        Sphere(int x, int y, int r) {
            this->x = x;
            this->y = y;
            this->r = r;
        }
        Sphere(int x, int y, int r, int dx, int dy) {
            this->x = x;
            this->y = y;
            this->r = r;
            this->dx = dx;
            this->dy = dy;
        }
        Sphere(int x, int y, int r, int dx, int dy,Color color) {
            this->x = x;
            this->y = y;
            this->r = r;
            this->dx = dx;
            this->dy = dy;
            this->color = color;
        }
        ~Sphere() {}
        
        // methods
        
        double getRadius() {
            return r;
        }

        pair<int,int> getLight() {
            return {lx,ly};
        }

        void updateLight() {
            lx = x-r;
            ly = y-r;
        }

        pair<Element*,double> detectNearestElement(vector<Element*>& elements) {
            double minDist = DBL_MAX;
            Element* res = nullptr;
            for (auto element : elements) {
                Sphere* s = dynamic_cast<Sphere*>(element);
                if (s!=nullptr && s!=this) {
                    auto pos = s->getPos();
                    double posX = pos.first;
                    double posY = pos.second;
                    
                    double dist = sqrt((posX-x)*(posX-x)+(posY-y)*(posY-y));
                    if (dist < minDist) {
                        minDist = dist;
                        res = element;
                    }
                }
            }
            return {res,minDist};
        }
};

struct Pixel {
    char c = ' ';
    Color color;
};

class Canvas {
    protected:
        int width = 20, height = 15;
        int lx = 8, ly = 8;
        vector<Element*> elements;
        vector<vector<Pixel>> canvas;
    public:
        Canvas() {
            for (int i = 0;i<height;i++) {
                canvas.push_back(vector<Pixel>());
                for (int j = 0;j<width;j++) {
                    if (i==0 && j==0) canvas[i].push_back({'+',RESET});
                    else if (i==0 && j==width-1) canvas[i].push_back({'+',RESET});
                    else if (i==height-1 && j==0) canvas[i].push_back({'+',RESET});
                    else if (i==height-1 && j==width-1) canvas[i].push_back({'+',RESET});
                    else if (i==0 || i==height-1) canvas[i].push_back({'-',RESET});
                    else if (j==0 || j==width-1) canvas[i].push_back({'|',RESET});
                    else canvas[i].push_back({' ',RESET});
                }
            }
        }
        ~Canvas() {}

        void clearCanvas() {
            resetConsoleColor();
            for (int i = 0;i<height;i++) {
                for (int j = 0;j<width;j++) {
                    if (i==0 && j==0) canvas[i][j] = {'+',RESET};
                    else if (i==0 && j==width-1) canvas[i][j] = {'+',RESET};
                    else if (i==height-1 && j==0) canvas[i][j] = {'+',RESET};
                    else if (i==height-1 && j==width-1) canvas[i][j] = {'+',RESET};
                    else if (i==0 || i==height-1) canvas[i][j] = {'-',RESET};
                    else if (j==0 || j==width-1) canvas[i][j] = {'|',RESET};
                    else canvas[i][j] = {' ',RESET};
                }
            }
        }

        void addSphere(double x, double y, double r) {
            elements.push_back(new Sphere(x,y,r));
        }

        void addSphere(double x, double y, double r, double vx, double vy) {
            elements.push_back(new Sphere(x,y,r,vx,vy));
        }
        void addSphere(double x, double y, double r, double vx, double vy,Color color) {
            elements.push_back(new Sphere(x,y,r,vx,vy,color));
        }

        void render() {
            clearCanvas();

            for (auto element : elements) {
                setConsoleColor(element->getColor());
                int x = element->getPos().first;
                int y = element->getPos().second;
                
                Sphere* s = dynamic_cast<Sphere*>(element);
                if (s!=nullptr) {
                    int r = s->getRadius();
                    int x = s->getPos().first;
                    int y = s->getPos().second;

                    for (int i = -r;i<=r;i++) {
                        for (int j = -r;j<=r;j++) {
                            if (i*i + j*j <= r*r) {
                                int cx = static_cast<int>(x-j);
                                int cy = static_cast<int>(y-i);
                                if (cx >= 0 && cx < width && cy>=0 && cy<height) {
                                    double distX = cx - s->getLight().first;
                                    double distY = cy - s->getLight().second;
                                    double dist = sqrt(distX*distX + distY*distY);
                                    double distRatio = dist/(r*3);
                                    distRatio = fmin(1.0, fmax(0.0, distRatio));
                                    int shadeIndex = static_cast<int>(distRatio*(s->getCharMap().size()-1));
                                    shadeIndex = fmin(s->getCharMap().size()-1,shadeIndex);
                                    canvas[cy][cx] = {s->getCharMap()[shadeIndex], s->getColor()};
                                }
                            }
                        }
                    }
                }
                resetConsoleColor();
            }

            for (int i = 0;i<height;i++) {
                for (int j = 0;j<width;j++) {
                    setConsoleColor(canvas[i][j].color);
                    cout << canvas[i][j].c << ' ';
                }
                cout << endl;
            }
        }

        void updateElements() {
            for (auto element : elements) {

                double x = element->getPos().first;
                double y = element->getPos().second;
                double dx = element->getVelocity().first;
                double dy = element->getVelocity().second;

                Sphere* s = dynamic_cast<Sphere*>(element);
                if (s!=nullptr) {
                    double r = s->getRadius();

                    auto elem = s->detectNearestElement(elements);
                    Element* nearestElem = elem.first;
                    double dist = elem.second;
                    
                    if (nearestElem!=nullptr) {
                        double oX = nearestElem->getPos().first;
                        double oY = nearestElem->getPos().second;
                        double oDx = nearestElem->getVelocity().first;
                        double oDy = nearestElem->getVelocity().second;
                        
                        Sphere* nearestSphere = dynamic_cast<Sphere*>(nearestElem);

                        if (nearestSphere!=nullptr) {
                            double oR = nearestSphere->getRadius();

                            double dxBetween = x-oX;
                            double dyBetween = y-oY;
                            double centerDist = sqrt(dxBetween * dxBetween + dyBetween * dyBetween);
                            if (centerDist < r + oR) {
                                // Normal vector (unit)
                                double angle = atan2(dyBetween, dxBetween);

                                dx = cos(angle);
                                dy = sin(angle);
                                s->setVelocity(dx,dy);
                                nearestSphere->setVelocity(oDx,oDy);
                            }
                        }
                    }

                    if (x-r<=0 || x+r>=width-1) {
                        dx = -0.8*dx;
                        if (x-r<=0) s->setPosition(r,y);
                        else if (x+r>=width-1) s->setPosition(width-1-r,y);
                    }
                    if (y-r<=0 || y+r>=height-1) {
                        dy = -0.8*dy;
                        if (y-r<=0) s->setPosition(x,r);
                        else if (y+r>=height-1) s->setPosition(x,height-1-r);
                    }

                    s->setVelocity(dx,dy);
                    s->updateLight();
                }

                element->update();
            }
        }
};

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> randomVel(-2,2);
    uniform_real_distribution<> randomRad(1,1);

    Canvas c;

    vector<Color> colors = {RED,YELLOW,GREEN,BLUE};


    // c.addSphere(10, 6, 2, 1, 0);
    // c.addSphere(20, 10, 3, -1, 0);
    // c.addSphere(25, 12, 4, -1, 0);

    int index = 0;
    for (int i = 0;i<2;i++) {
        for (int j = 0;j<2;j++) {
            c.addSphere(6+j*6, 6+i*4, randomRad(gen), randomVel(gen), randomVel(gen),colors[(index++)%colors.size()]);
        }
    }


    while (true) {
        cout << "\033[2J\033[H";  // clear screen
        c.render();
        c.updateElements();
        this_thread::sleep_for(chrono::milliseconds(50));
    }

    return 0;
}
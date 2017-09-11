CXXFLAGS := -W -Wall -Wextra -Wconversion -march=native -O3 --std=c++11
TARGETS := sdes libsdes.so

all: $(TARGETS)

libsdes.so: sdes.cpp
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -shared -fPIC -fvisibility=default -fPIC $< -o$@

run:
	pypy mono.py cipher-mono.txt

check: libsdes.so
	python compare.py

clean:
	rm -f $(TARGETS)

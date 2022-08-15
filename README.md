# Wave Function Collapse

This is a simple implementation of the Wave Function Collapse algoritm using tiles.

The input images must be named `{id}_{constraints}.png` where:
* `id` is a unique string identifier accross the images
* `constraints` is the concatenation of `up`, `right`, `bottom`, and `left` constraints
    * Each of these constraints is a string of some arbitrary size, as long as all 4 constraints have the same size. Therefore, `len(constraints) % 4 == 0`.
    * These constraints will act as sockets to decide which tiles can be plugged to other tiles
* Each image in the set will be rotated 3 times to produce more images

## Examples

### Circuit

#### Input

![image](images/circuit/0_000000000000.png)
![image](images/circuit/1_111111111111.png)
![image](images/circuit/2_111121111111.png)
![image](images/circuit/3_111131111131.png)
![image](images/circuit/4_011121011000.png)
![image](images/circuit/5_011111111011.png)
![image](images/circuit/6_111121111121.png)
![image](images/circuit/7_131121131121.png)
![image](images/circuit/8_131111121111.png)
![image](images/circuit/9_121121111121.png)
![image](images/circuit/10_121121121121.png)

#### Output

![image](output/circuit.png)

### Circle

#### Input

![image](images/circle/0_1000.png)
![image](images/circle/1_1010.png)
![image](images/circle/2_1100.png)
![image](images/circle/3_1111.png)
![image](images/circle/4_0111.png)
![image](images/circle/5_0101.png)
![image](images/circle/6_0011.png)
![image](images/circle/7_0000.png)

#### Output

![image](output/circle.png)

### Track

#### Input

![image](images/track/0_0000.png)
![image](images/track/1_0111.png)

#### Output

![image](output/track.png)
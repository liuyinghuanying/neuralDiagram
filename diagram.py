import numpy as np
from matplotlib import pyplot as plt


x_r = 6
x_l = -6
w_a = x_r - x_l

y_t = x_r
y_b = x_l
h_a = y_t - y_b

if x_r > 10:
    dist_x = (np.abs(x_l)*2)*0.08
    dist_y = (np.abs(y_t)*2)*0.15
    w = (np.abs(x_l)*2)*0.14
    radius = ((np.abs(y_t) + np.abs(y_b)) * (np.abs(x_l) + np.abs(x_r)) * 0.3) /500.0
else:
    dist_x = 1
    dist_y = 2
    w = 1
    radius = 0.3

fig = plt.figure(facecolor='w')
ax = fig.add_axes([0, 0, 1, 1],
                  xticks=[], yticks=[])
INPUT_L_X = x_l + dist_x
OUTPUT_L_X = x_r -dist_x
layers_x = []

plt.box(False)
#circ = plt.Circle((1, 1), 8)
arrow_kwargs = dict(head_width=0.05, fc='black')


def draw_connecting_arrow(ax, circ1, rad1, circ2, rad2):
    theta = np.arctan2(circ2[1] - circ1[1],
                       circ2[0] - circ1[0] )

    starting_point = ((circ1[0] + radius),
                      circ1[1] )

    length = (circ2[0] - circ1[0] - 0.9*radius - (rad1 + 1.4 * rad2) * np.cos(theta),
              circ2[1] - circ1[1] - (rad1 + 1.4 * rad2) * np.sin(theta))

    ax.arrow(starting_point[0], starting_point[1],
             length[0], length[1], head_width = radius/3.0, head_length = radius/3.0)


# function to draw circles
def draw_circle(ax, center, radius):
    circ = plt.Circle(center, radius, fc='none', lw=2)
    ax.add_patch(circ)


def x_aved(layer_number):
    return ((w_a - (2 * dist_x)) / layer_number)


def y_aved(neurons):
    return (h_a - (2 * dist_y)) / neurons


def drawer(in_neurons, out_neurons, hi_layers, hi_neurons):
# Draw the Input layer
    hi_neuron_xs = []
    hi_neuron_ys = []
    output_y = []
    input_y = []
    for i, input_i_y in enumerate(np.linspace(y_t - dist_y, y_b + dist_y, in_neurons)):
        input_y.append(input_i_y)
        draw_circle(ax, (x_l + dist_x, input_i_y), radius)
        ax.text((x_l + dist_x) -0.8* w, input_i_y, "Input #%i" % (i + 1),
                ha="right", va="center", fontsize=12)
        draw_connecting_arrow(
            ax, ((x_l + dist_x - w), input_i_y), 0.1, ((x_l + dist_x), input_i_y), radius)

# Draw the Output layer
    if out_neurons != 1:
        for i, output_i_y in enumerate(np.linspace(y_t - dist_y, y_b + dist_y, out_neurons)):
            output_y.append(output_i_y)
            draw_circle(ax, (x_r - dist_x, output_i_y), radius)
            ax.text((x_r - dist_x)+0.8*w , output_i_y, "Output #%i" % (i + 1),
                    ha="left", va="center", fontsize=12)
            draw_connecting_arrow(
                ax, ((x_r - dist_x ), output_i_y), 0.1, ((x_r - dist_x + w), output_i_y), radius)
    elif out_neurons ==1:
        output_y = [0]
        draw_circle(ax, (x_r - dist_x, 0), radius)
        ax.text((x_r - dist_x) + w, 0, "Output #%i" % (i + 1),
                ha="left", va="center", fontsize=12)
# Draw hidden layer

#   When there is only one hidden layer:
    if hi_layers == 1 and hi_neurons != 1:
        hi_neuron_xs = [0]
        x_1 = x_l + dist_x
        x_2 = 0
        x_3 = x_r - dist_x
        for hi_neuron_y in np.linspace(y_t - dist_y, y_b + dist_y, hi_neurons):
            draw_circle(ax, (x_2, hi_neuron_y), radius)
            for i, input_i_y in enumerate(np.linspace(y_t - dist_y, y_b + dist_y, in_neurons)):
                draw_connecting_arrow(ax, (x_1, input_i_y), 0.1, (x_2, hi_neuron_y), radius)
                if out_neurons == 1:
                    draw_connecting_arrow(
                        ax, (x_2, hi_neuron_y), 0.1, ((x_3, 0), radius))
                else:
                    for _, out_i_y in enumerate(np.linspace (y_t - dist_y, y_b + dist_y, out_neurons)):
                        draw_connecting_arrow(ax, (x_2, hi_neuron_y), 0.1, (x_3, out_i_y), radius)

# When there are more than 1 hidden layer:
    elif hi_layers != 1 and hi_neurons != 1:
        hi_neuron_xs = []
        hi_neuron_ys = []
        for hi_neuron_x in np.linspace(x_l + 3 * dist_x, x_r - 3 * dist_x, hi_layers):
            hi_neuron_xs.append(hi_neuron_x)
        for hi_neuron_y in np.linspace(y_t - dist_y, y_b + dist_y, hi_neurons):
            hi_neuron_ys.append(hi_neuron_y)
        for x in hi_neuron_xs:
            for y in hi_neuron_ys:
                print x, y
                draw_circle(ax, (x, y), radius)
# Draw the arrow between hidden neurons
        for i, _ in enumerate(hi_neuron_xs):
            for j, _ in enumerate(hi_neuron_ys):
                for k, _ in enumerate(hi_neuron_ys):
                    try:
                        draw_connecting_arrow(ax, (hi_neuron_xs[i], hi_neuron_ys[j]),
                                              0.1, (hi_neuron_xs[1 + i], hi_neuron_ys[k]), radius)
                    except:
                        print "done"
    elif hi_layers == 1 and hi_neurons ==1:
        print "Not yet"

# Connect the input layer to first hidden layer
    for iy in input_y:
        for hy in hi_neuron_ys:
            draw_connecting_arrow(ax, (INPUT_L_X, iy), 0.1, (hi_neuron_xs[0], hy), radius)
# Connect the last hidden layer to the output layer
    for iy in output_y:
        for hy in hi_neuron_ys:
            draw_connecting_arrow(ax, (hi_neuron_xs[-1], hy), 0.1, (OUTPUT_L_X, iy), radius)



plt.text(x_l + dist_x, y_t - 0.5, "Input\nLayer", ha='center', va='top', fontsize=12)
plt.text(0, y_t - 0.5, "Hidden Layer", ha='center', va='top', fontsize=12)
plt.text(x_r - dist_x, y_t - 0.5, "Output\nLayer",
         ha='center', va='top', fontsize=12)

drawer(4, 1, 3, 6)
ax.set_aspect('equal')
plt.xlim(x_l, x_r)
plt.ylim(y_b, y_t)
plt.show()

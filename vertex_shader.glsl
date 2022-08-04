#version 330

in vec2 in_pos;

in vec3 in_color;

in float in_alpha;

out vec4 color;

void main() {

    color = vec4(in_color, in_alpha);

    gl_Position = vec4(in_pos, 0, 1);

}
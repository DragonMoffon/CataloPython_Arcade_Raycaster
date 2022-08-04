#version 330

uniform float walls[641];
uniform float textures[641];
uniform sampler2D ourTexture;

in vec2 in_pos;

void main()
{
    // Set the position. (x, y, z, w)
    gl_Position = vec4(in_pos, 0, 1);
}
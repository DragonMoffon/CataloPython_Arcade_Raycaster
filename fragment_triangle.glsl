#version 330

uniform sampler2D brickTexture;
uniform float wall_x[641];
uniform float wall_height[641];


in vec4 gl_FragCoord;

out vec4 fragColor;

void main()
{
    int index = int(gl_FragCoord.x);
    if (gl_FragCoord.y < 320 + wall_height[index]/2 && gl_FragCoord.y > 320 - wall_height[index]/2)
    {
       float y = float( int(gl_FragCoord.y - 320 + wall_height[index]) & (640 - 1))/640;
       fragColor = texture(brickTexture, vec2(wall_x[index]/640, y));
    }
    else
    {
       fragColor = vec4(0);
    }

}
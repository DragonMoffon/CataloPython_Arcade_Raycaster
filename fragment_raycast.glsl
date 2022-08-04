#version 330

in vec4 gl_FragCoord;

out vec4 fragColor;

uniform sampler2D map1;
uniform dvec4 pos;
uniform dvec2 resolution;

double camera_x = double(2.0) * (double(gl_FragCoord.x)/resolution.x) - double(1.0);
dvec2 ray_dir = dvec2(pos.xy) + dvec2(pos.zw) * camera_x;
ivec2 map_pos = ivec2(pos.xy);

dvec2 sideDist;
dvec2 deltaDist = abs(1 / dvec2(ray_dir));
double perpWallDist;

ivec2 step;
int side;


void main()
{
    if (ray_dir.x < 0)
    {
        step.x = -1;
        sideDist.x = (pos.x - map_pos.x) * deltaDist.x;
    }
    else
    {
        step.x = 1;
        sideDist.x = (map_pos.x + 1.0 - pos.x) * deltaDist.x;
    }
    if (ray_dir.y < 0)
    {
        step.y = -1;
        sideDist.y = (pos.y - map_pos.y) * deltaDist.y;
    }
    else
    {
        step.y = 1;
        sideDist.y = (map_pos.y + 1.0 - map_pos.y) * deltaDist.y;
    }

    bool hit = false;

    while (!hit)
    {
        if (sideDist.x < sideDist.y)
        {
            sideDist.x += deltaDist.x;
            map_pos.x += step.x;
            side = 0;
        }
        else
        {
            sideDist.y += deltaDist.y;
            map_pos.y += step.y;
            side = 1;
        }

        if (texture(map1, map_pos/32).x > 0)
        {
            hit = true;
        }
    }

    if (side == 0) perpWallDist = (map_pos.x - pos.x + (1 - step.x) / 2) / ray_dir.x;
    else perpWallDist = (map_pos.y - pos.y + (1 - step.y) / 2) / ray_dir.y;

    double lineHeight = resolution.y / perpWallDist;

    double draw_start = -lineHeight / 2.0 + resolution.y / 2.0;
    if (draw_start < 0) draw_start = 0.0;

    double draw_end = lineHeight/2 + resolution.y / 2;
    if (draw_end >= resolution.y) draw_end = resolution.y - 1.0;

    if (gl_FragCoord.y >= draw_start && gl_FragCoord.y <= draw_end) fragColor = texture(map1, map_pos/32);
    else fragColor = vec4(0, 0, 0, 0);
}
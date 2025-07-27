#version 450

layout (binding = 1) uniform sampler2DArray texture_samplers;
layout (location = 0) in vec3 input_fragment_texture_coordinates;
layout (location = 0) out vec4 output_fragment_colour;

void main() {
	output_fragment_colour = texture(texture_samplers, input_fragment_texture_coordinates);
}
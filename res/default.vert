#version 450

layout (binding = 0) uniform UBO {
	mat4 view;
	mat4 projection;
} ubo;

layout (location = 0) in vec3 input_coordinates;
layout (location = 1) in vec3 input_colour;
layout (location = 2) in vec2 input_texture_coordinates;
layout (location = 3) in vec3 input_instance_translation;
layout (location = 4) in vec4 input_instance_rotation;
layout (location = 5) in vec3 input_instance_scale;
layout (location = 6) in uint input_instance_texture_index;
layout (location = 0) out vec3 output_fragment_colour;
layout (location = 1) out vec3 output_fragment_texture_coordinates;

mat4 translation_vector_to_matrix(const vec3 v) {
	return mat4(
		1.0, 0.0, 0.0, 0.0,
		0.0, 1.0, 0.0, 0.0,
		0.0, 0.0, 1.0, 0.0,
		v.x, v.y, v.z, 1.0
	);
}
mat4 scale_vector_to_matrix(const vec3 v) {
	return mat4(
		v.x, 0.0, 0.0, 0.0,
		0.0, v.y, 0.0, 0.0,
		0.0, 0.0, v.z, 0.0,
		0.0, 0.0, 0.0, 1.0
	);
}

float quaternion_multiply_x(const vec4 lhs, const vec4 rhs) {
 return
  lhs.x * rhs.w +
  lhs.y * rhs.z -
  lhs.z * rhs.y +
  lhs.w * rhs.x;
}
float quaternion_multiply_y(const vec4 lhs, const vec4 rhs) {
 return
  lhs.y * rhs.w -
  lhs.x * rhs.z +
  lhs.w * rhs.y +
  lhs.z * rhs.x;
}
float quaternion_multiply_z(const vec4 lhs, const vec4 rhs) {
 return
  lhs.z * rhs.w +
  lhs.w * rhs.z +
  lhs.x * rhs.y -
  lhs.y * rhs.x;
}
float quaternion_multiply_w(const vec4 lhs, const vec4 rhs) {
 return
  lhs.w * rhs.w -
  lhs.z * rhs.z -
  lhs.y * rhs.y -
  lhs.x * rhs.x;
}
vec4 quaternion_multiply(const vec4 lhs, const vec4 rhs) {
 return vec4(
  quaternion_multiply_x(lhs, rhs),
  quaternion_multiply_y(lhs, rhs),
  quaternion_multiply_z(lhs, rhs),
  quaternion_multiply_w(lhs, rhs)
 );
}

mat4 quaternion_to_rotation_matrix(const vec4 quaternion) {
 const float squares = 2.0 / (
  quaternion.x * quaternion.x +
  quaternion.y * quaternion.y +
  quaternion.z * quaternion.z +
  quaternion.w * quaternion.w
 );
 const float x_squares = quaternion.x * squares;
 const float y_squares = quaternion.y * squares;
 const float z_squares = quaternion.z * squares;
 const float xx_squares = quaternion.x * x_squares;
 const float xy_squares = quaternion.x * y_squares;
 const float xz_squares = quaternion.x * z_squares;
 const float yy_squares = quaternion.y * y_squares;
 const float yz_squares = quaternion.y * z_squares;
 const float zz_squares = quaternion.z * z_squares;
 const float wx_squares = quaternion.w * x_squares;
 const float wy_squares = quaternion.w * y_squares;
 const float wz_squares = quaternion.w * z_squares;

 return mat4(
  1.0 - yy_squares - zz_squares, xy_squares - wz_squares      , xz_squares + wy_squares      , 0.0,
  xy_squares + wz_squares      , 1.0 - xx_squares - zz_squares, yz_squares - xy_squares      , 0.0,
  xz_squares - wy_squares      , yz_squares + wx_squares      , 1.0 - xx_squares - yy_squares, 0.0,
  0.0                          , 0.0                          , 0.0                          , 1.0
 )
}

void main() {
 const mat4 instance_transformation = 
  translation_vector_to_matrix(instanced_translation) * 
  quaternion_to_rotation_matrix(instanced_rotation) *
  scale_vector_to_matrix(instanced_scale) *
  vec4(vertex_XYZ, 1.0);

 gl_Position = 
  ubo.projection * 
  ubo.view * 
  instance_transformation;
}
#define number_t double

typedef struct vec3d_t {
	number_t x;
	number_t y;
	number_t z;
} vec3d_t;

void vec3d_copy(vec3d_t *a, vec3d_t *b);

void vec3d_set(vec3d_t *a, number_t x, number_t y, number_t z);

void vec3d_add(vec3d_t *a, vec3d_t *b, vec3d_t *c);

void vec3d_iadd(vec3d_t *a, vec3d_t *b);

void vec3d_sub(vec3d_t *a, vec3d_t *b, vec3d_t *c);

void vec3d_isub(vec3d_t *a, vec3d_t *b);

void vec3d_mul(vec3d_t *a, vec3d_t *b, number_t scalor);

void vec3d_imul(vec3d_t *a, number_t scalor);

void vec3d_div(vec3d_t *a, vec3d_t *b, number_t scalor);

void vec3d_idiv(vec3d_t *a, number_t scalor);

number_t vec3d_dot(vec3d_t *a, vec3d_t *b);

void vec3d_cross(vec3d_t *a, vec3d_t *b, vec3d_t *c);

number_t vec3d_magnitude(vec3d_t *a);

number_t vec3d_distance(vec3d_t *a, vec3d_t *b);

double vec3d_interior_angle(vec3d_t *a, vec3d_t *b);

double vec3d_angle(vec3d_t *a, vec3d_t *b, vec3d_t *normal);

void vec3d_rotate_x(vec3d_t *a, vec3d_t *b, double angle);

void vec3d_irotate_x(vec3d_t *a, double angle);

void vec3d_rotate_y(vec3d_t *a, vec3d_t *b, double angle);

void vec3d_irotate_y(vec3d_t *a, double angle);

void vec3d_rotate_z(vec3d_t *a, vec3d_t *b, double angle);

void vec3d_rotate(vec3d_t *a, vec3d_t *b, vec3d_t *axis, double angle);
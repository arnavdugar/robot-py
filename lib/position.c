#include "position.h"
#include "math.h"
#include <stdio.h>

void vec3d_copy(vec3d_t *a, vec3d_t *b) {
    a->x = b->x;
    a->y = b->y;
    a->z = b->z;
}

void vec3d_set(vec3d_t *a, number_t x, number_t y, number_t z) {
    a->x = x;
    a->y = y;
    a->z = z;
}

void vec3d_add(vec3d_t *a, vec3d_t *b, vec3d_t *c) {
    a->x = b->x + c->x;
    a->y = b->y + c->y;
    a->z = b->z + c->z;
}

void vec3d_iadd(vec3d_t *a, vec3d_t *b) {
    vec3d_add(a, a, b);
}

void vec3d_sub(vec3d_t *a, vec3d_t *b, vec3d_t *c) {
    a->x = b->x - c->x;
    a->y = b->y - c->y;
    a->z = b->z - c->z;
}

void vec3d_isub(vec3d_t *a, vec3d_t *b) {
    vec3d_sub(a, a, b);
}

void vec3d_mul(vec3d_t *a, vec3d_t *b, number_t scalor) {
    a->x = b->x * scalor;
    a->y = b->y * scalor;
    a->z = b->z * scalor;
}

void vec3d_imul(vec3d_t *a, number_t scalor) {
    vec3d_mul(a, a, scalor);
}

void vec3d_div(vec3d_t *a, vec3d_t *b, number_t scalor) {
    a->x = b->x / scalor;
    a->y = b->y / scalor;
    a->z = b->z / scalor;
}

void vec3d_idiv(vec3d_t *a, number_t scalor) {
    vec3d_div(a, a, scalor);
}

number_t vec3d_dot(vec3d_t *a, vec3d_t *b) {
    return a->x * b->x + a->y * b->y + a->z * b->z;
}

void vec3d_cross(vec3d_t *a, vec3d_t *b, vec3d_t *c) {
    number_t x = b->y * c->z - b->z * c->y;
    number_t y = b->z * c->x - b->x * c->z;
    number_t z = b->x * c->y - b->y * c->x;
    vec3d_set(a, x, y, z);
}

number_t vec3d_magnitude(vec3d_t *a) {
    return sqrt(vec3d_dot(a, a));
}

void vec3d_normalize(vec3d_t *a, vec3d_t *b) {
    vec3d_div(a, b, vec3d_magnitude(b));
}

void vec3d_inormalize(vec3d_t *a) {
    vec3d_idiv(a, vec3d_magnitude(a));
}

number_t vec3d_distance(vec3d_t *a, vec3d_t *b) {
    vec3d_t difference;
    vec3d_sub(&difference, a, b);
    return vec3d_magnitude(&difference);
}

double vec3d_interior_angle(vec3d_t *a, vec3d_t *b) {
    number_t dot = vec3d_dot(a, b);
    number_t norm = sqrt(vec3d_dot(a, a) * vec3d_dot(b, b));
    return acos(dot / norm);
}

double vec3d_angle(vec3d_t *a, vec3d_t *b) {
    vec3d_t cross;
    vec3d_cross(&cross, a, b);
    number_t dot = vec3d_dot(a, b);
    return atan2(vec3d_magnitude(&cross), dot);
}

void vec3d_rotate_x(vec3d_t *a, vec3d_t *b, double angle) {
    number_t y = b->y * cos(angle) - b->z * sin(angle);
    number_t z = b->y * sin(angle) + b->z * cos(angle);
    vec3d_set(a, b->x, y, z);
}

void vec3d_irotate_x(vec3d_t *a, double angle) {
    vec3d_rotate_x(a, a, angle);
}

void vec3d_rotate_y(vec3d_t *a, vec3d_t *b, double angle) {
    number_t z = b->z * cos(angle) - b->x * sin(angle);
    number_t x = b->z * sin(angle) + b->x * cos(angle);
    vec3d_set(a, x, b->y, z);
}

void vec3d_irotate_y(vec3d_t *a, double angle) {
    vec3d_rotate_y(a, a, angle);
}

void vec3d_rotate_z(vec3d_t *a, vec3d_t *b, double angle) {
    number_t x = b->x * cos(angle) - b->y * sin(angle);
    number_t y = b->x * sin(angle) + b->y * cos(angle);
    vec3d_set(a, x, y, b->z);
}

void vec3d_irotate_z(vec3d_t *a, double angle) {
    vec3d_rotate_z(a, a, angle);
}

void vec3d_rotate(vec3d_t *a, vec3d_t *b, vec3d_t *axis, double angle) {
    vec3d_t value, temp;
    double c = cos(angle), s = sin(angle);
    vec3d_mul(&value, b, c);
    vec3d_cross(&temp, axis, b);
    vec3d_imul(&temp, s);
    vec3d_iadd(&value, &temp);
    vec3d_mul(&temp, axis, (1 - c) * vec3d_dot(b, axis));
    vec3d_add(a, &value, &temp);
}
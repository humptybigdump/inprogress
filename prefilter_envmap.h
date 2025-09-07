#pragma once

#include <memory>
#include <glm/glm.hpp>

class Image;
class ImageTexture;


glm::vec2 lonlat_coordf_from_direction(glm::vec3 dir, glm::ivec2 size);
glm::ivec2 lonlat_coord_from_direction(glm::vec3 dir, glm::ivec2 size);
glm::vec3 direction_from_lonlat_coord(glm::ivec2 c, glm::ivec2 size);
float solid_angle_from_lonlat_coord(glm::ivec2 c, glm::ivec2 size);

std::shared_ptr<Image> prefilter_environment_diffuse(Image const& img);
std::shared_ptr<Image> prefilter_environment_specular(Image const& img, float n);
void resample_to_cubemap(ImageTexture const& lonlatmap);


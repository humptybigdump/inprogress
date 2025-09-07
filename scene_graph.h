#pragma once

#include <glm/glm.hpp>
#include <vector>
#include <memory>

class GLObjModel;

// Helper struct
struct TransformedModel {
	glm::mat4 object_to_world = glm::mat4(1.0f);
	glm::mat4 world_to_object = glm::mat4(1.0f);
	GLObjModel* model;

	TransformedModel(const glm::mat4& object_to_world_, const glm::mat4& world_to_object_, GLObjModel* model_) :
		object_to_world(object_to_world_),
		world_to_object(world_to_object_),
		model(model_)
	{}
};

// Scene graph for sphere flake (and more?)
class SceneGraphNode
{
public:
	glm::mat4 node_to_parent = glm::mat4(1.0f);
	glm::mat4 parent_to_node = glm::mat4(1.0f);
	std::vector<std::shared_ptr<SceneGraphNode>> children;
	std::shared_ptr<GLObjModel> model;

	void collectTransformedModels(std::vector<TransformedModel>& transformed_models, const glm::mat4& parent_to_world = glm::mat4(1.f), const glm::mat4& world_to_parent = glm::mat4(1.f)) const;
};

std::shared_ptr<SceneGraphNode>
buildSphereFlakeSceneGraph(
		const std::shared_ptr<GLObjModel>& model,
		float sphere_model_radius,
		float size_factor,
		int number_of_remaining_recursions);

void animateSphereFlake(SceneGraphNode& root, float angle_increment);

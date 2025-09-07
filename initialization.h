#ifndef INITIALIZATION
#define INITIALIZATION
#include <vulkan/vulkan.hpp>
#include <cstring>
#include <GLFW/glfw3.h>

#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_vulkan.h"

struct AppResources
{
    vk::Instance instance;
    vk::DebugUtilsMessengerEXT dbgUtilsMgr;
    vk::PhysicalDevice pDevice;

    vk::Device device;
    vk::Queue graphicsQueue, computeQueue, transferQueue;
    uint32_t gQ, cQ, tQ;
    vk::CommandPool graphicsCommandPool, computeCommandPool, transferCommandPool;
    vk::QueryPool queryPool;

    GLFWwindow* window;
    vk::Extent2D extent;
    vk::SurfaceKHR surface;
    vk::SurfaceFormatKHR surfaceFormat;
    vk::SwapchainKHR swapchain;
    std::vector<vk::Image> swapchainImages;
    std::vector<vk::ImageView> swapchainImageViews;

    void destroy();
};

VKAPI_ATTR VkBool32 VKAPI_CALL
debugUtilsMessengerCallback(VkDebugUtilsMessageSeverityFlagBitsEXT messageSeverity,
                            VkDebugUtilsMessageTypeFlagsEXT messageTypes,
                            VkDebugUtilsMessengerCallbackDataEXT const *pCallbackData,
                            void * /*pUserData*/);
vk::DebugUtilsMessengerCreateInfoEXT makeDebugUtilsMessengerCreateInfoEXT();

void selectPhysicalDevice(vk::Instance &instance, vk::PhysicalDevice &pDevice);
void createInstance(vk::Instance &instance, vk::DebugUtilsMessengerEXT &debugUtilsMessenger,
                    std::string appName, std::string engineName, bool headless);
void createLogicalDevice(vk::Instance &instance, vk::PhysicalDevice &pDevice, vk::Device &device, bool withWindow);
std::tuple<uint32_t, uint32_t, uint32_t> getGCTQueues(vk::PhysicalDevice &pDevice);
void createCommandPool(vk::Device &device, vk::CommandPool &commandPool, uint32_t queueIndex);
void destroyInstance(vk::Instance &instance, vk::DebugUtilsMessengerEXT &debugUtilsMessenger);
void destroyLogicalDevice(vk::Device &device);
void destroyCommandPool(vk::Device &device, vk::CommandPool &commandPool);

void createTimestampQueryPool(vk::Device &device, vk::QueryPool &queryPool, uint32_t queryCount);
void destroyQueryPool(vk::Device &device, vk::QueryPool &queryPool);

void createSwapchain(AppResources &app);

void printDeviceCapabilities(vk::PhysicalDevice &pDevice);

void initApp(AppResources &app, bool withWindow = false, const std::string& name = "GPGPU/GPU-C", int width = 800, int height = 600);
#endif

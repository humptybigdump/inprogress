#define USE_TWEAK_BAR
#include <array>

#include "stdafx.h"
#include "defines.h"
#include "twbar_builder.h"

#define CG_SOLUTION

#define EXERCISE_DIR "./Assignments/InCG-DoF/"
#define ASSETS_DIR "./data/"
#define SHADER_DIR EXERCISE_DIR "shader/"

char applicationTitle[128] = "Depth of Field";
const char path2Demo[] = "Assignments/InCG-DoF/";
static constexpr int max_layers = 32;

TwBar *bar = nullptr;

struct Params {
    float exposure = 0.f;
    int num_layers = 16;
    bool show_individual_layer = false;
    bool show_depth_vs = false;
    bool copy_fragments = true;
    int layer_to_show = 0;

    float focal_length = 0.250f;
    float f_stop = 1.2f;
    float d_f = 1.5f;
    float layer_overlap = 0.1;
    float dof_strength = 1000;

    int dof_samples = 16;
} params;

void initializeTweakBar() {
    nTweakBarVariables = 0;

    TwInit(TW_OPENGL, nullptr);
    TwDefine("GLOBAL fontsize=3");

    auto wrapper = TwBarWrapper(bar, "DepthOfField");
    wrapper.addInteger("num_layers", &params.num_layers)
            ->set_label("Layer Count")
            ->set_help("How many layers the scene should be divided into for depth of field rendering")
            ->set_min("1")
            ->set_max(std::to_string(max_layers))
            ->set_step("1")
            ->set_group("Decomposition");

    wrapper.addBoolean("show_individual_layer", &params.show_individual_layer)
            ->set_label("Show individual layers")
            ->set_help("Show a single individual rendered layer from the scene decomposition")
            ->set_group("Decomposition");

    wrapper.addInteger("layer_to_show", &params.layer_to_show)
            ->set_label("Layer Index")
            ->set_help("The index of the scene decomposition layer to show when \"Show individual layers\" is enabled")
            ->set_group("Decomposition");

    wrapper.addBoolean("copy_fragments", &params.copy_fragments)
            ->set_label("Copy fragments")
            ->set_help("Copy fragments into their appropriate layer from the scene decomposition")
            ->set_group("Decomposition");


    wrapper.addFloat("layer_overlap", &params.layer_overlap)
            ->set_label("Layer Overlap")
            ->set_min("0")
            ->set_max("1")
            ->set_step("0.02")
            ->set_help("Percentage of layer overlap to remove seam artifacts")
            ->set_group("Decomposition");

    wrapper.addBoolean("show_pos_ws", &params.show_depth_vs)
            ->set_label("Show World Position")
            ->set_help("Show World Position from the scene decomposition")
            ->set_group("View");

    wrapper.addFloat("focal_length", &params.focal_length)
            ->set_label("Focal Length (m)")
            ->set_help("Thin lens focal length (distance between lens and sensor)")
            ->set_min("0.001")
            ->set_max("1")
            ->set_step("0.005")
            ->set_group("Camera");

    wrapper.addFloat("f_stop", &params.f_stop)
            ->set_label("F-Stop")
            ->set_help(
                "Aperture f-stop (lower f stop means bigger aperture means shallower depth of field means more blur)")
            ->set_min("0.1")
            ->set_max("24")
            ->set_step("0.1")
            ->set_group("Camera");

    wrapper.addFloat("d_f", &params.d_f)
            ->set_label("Focus plane (m)")
            ->set_help("Distance of the focus plane in meters")
            ->set_min("1")
            ->set_max("100")
            ->set_step("0.1")
            ->set_group("Camera");

    wrapper.addFloat("dof_strength", &params.dof_strength)
            ->set_label("DoF Strength")
            ->set_help("Arbitrary factor to control the strength of the DoF effect")
            ->set_min("0")
            ->set_max("1000")
            ->set_step("1")
            ->set_group("Camera");

    wrapper.addInteger("dof_samples", &params.dof_samples)
            ->set_label("DoF Samples")
            ->set_help("Number of samples for the DoF effect")
            ->set_min("1")
            ->set_max("128")
            ->set_step("1")
            ->set_group("Camera");
}

class CRender final : public CRenderBase {
public:
    std::shared_ptr<Scene> scene = nullptr;

    GLSLProgram render_layers_program;
    GLSLProgram blit_layer_program;
    GLSLProgram blit_program;
    GLSLProgram copy_fragments_program;
    GLSLProgram combine_layers_program;

    Camera camera;
    GLuint vao_empty;

    CRender() {
        glfwGetWindowSize(glfwWindow, &width, &height);
        CRenderBaseInit();

        camera.camNear = 0.5f;
        camera.camFar = 100.0f;

        this->loadShaders(true);
        this->createFramebuffers();

        const char *attribs[3] = {
            "POSITION",
            "NORMAL",
            "TEXCOORD"
        };

        mat4x4 model = scale(mat4(1), vec3(10));
        scene = std::make_shared<Scene>(texMan);
        scene->loadOBJ(
            SCENE_SMOOTH | SCENE_TEXTURE,
            render_layers_program.getProgramObject(),
            3,
            attribs,
            "sponza_triag.obj",
            ASSETS_DIR "crytek-sponza/",
            true,
            &model
        );

        glGenVertexArrays(1, &vao_empty);
    }

    GLuint layered_fbo;
    GLuint layered_color;
    GLuint layered_depth_vs;
    GLuint layered_depth;
    GLuint combined_image;

    void createFramebuffers() {
        if (layered_fbo != 0) {
            glDeleteFramebuffers(1, &layered_fbo);
        }
        glGenFramebuffers(1, &layered_fbo);
        glBindFramebuffer(GL_FRAMEBUFFER, layered_fbo);

        if (layered_color != 0) {
            glDeleteTextures(1, &layered_color);
        }
        glGenTextures(1, &layered_color);
        glBindTexture(GL_TEXTURE_2D_ARRAY, layered_color);
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA8, width, height, params.num_layers, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     nullptr);
        CheckErrorsGL();

        if (layered_depth_vs != 0) {
            glDeleteTextures(1, &layered_depth_vs);
        }
        glGenTextures(1, &layered_depth_vs);
        glBindTexture(GL_TEXTURE_2D_ARRAY, layered_depth_vs);
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_R32F, width, height, params.num_layers, 0, GL_RED, GL_FLOAT, nullptr);
        CheckErrorsGL();

        if (layered_depth != 0) {
            glDeleteTextures(1, &layered_depth);
        }
        glGenTextures(1, &layered_depth);
        glBindTexture(GL_TEXTURE_2D_ARRAY, layered_depth);
        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_DEPTH_COMPONENT32F, width, height, params.num_layers, 0,
                     GL_DEPTH_COMPONENT,GL_FLOAT, nullptr);
        CheckErrorsGL();

        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, layered_color, 0);
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, layered_depth_vs, 0);
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, layered_depth, 0);
        CheckErrorsGL();

        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
            std::cerr << "Failed to create layered framebuffer" << std::endl;
            exit(1);
        }

        glBindFramebuffer(GL_FRAMEBUFFER, 0);

        if (combined_image != 0) {
            glDeleteTextures(1, &combined_image);
        }
        glGenTextures(1, &combined_image);
        glBindTexture(GL_TEXTURE_2D, combined_image);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, nullptr);
        CheckErrorsGL();

        glBindTexture(GL_TEXTURE_2D, 0);
    }

    void windowSizeChanged(const int width, const int height) {
        if (width <= 0 || height <= 0) {
            return;
        }
        this->width = width;
        this->height = height;
        this->createFramebuffers();
    }

    float calcLayerBoundary(const int layer_index) const {
        const float ratio = static_cast<float>(layer_index) / static_cast<float>(params.num_layers) *
                            (1.f - camera.camNear / camera.camFar);
        return camera.camNear / (1.f - ratio);
    }

    void loadShaders(const bool firstTime) override {
#ifdef USE_TWEAK_BAR
        initializeTweakBar();
#endif

        Defines defines;

#define program_add_shader(program, shader_type, asset, extra_defines) do { \
        if (!program.load ## shader_type ## Shader(const_cast<char *>(SHADER_DIR asset), (defines + extra_defines).toString().c_str())) { \
            if (firstTime) { \
                std::cerr << "Failed to load shader \"" << asset << "\"" << std::endl; \
                exit(1); \
            } \
        } \
    } while(false)

#define program_link(program) do { \
        if (!program.link()) { \
            std::cerr << "Failed to link program \"" << #program << "\"" << std::endl; \
            if (firstTime) exit(1); \
        } \
    } while(false)

#define program_vert_frag_def(program, vert_shader, frag_shader, extra_defines) do { \
    program_add_shader(program, Vertex, vert_shader, extra_defines); \
    program_add_shader(program, Fragment, frag_shader, extra_defines); \
    program_link(program); \
    } while(false)

#define program_vert_frag(program, vert_shader, frag_shader) program_vert_frag_def(program, vert_shader, frag_shader, Defines())

#define program_vert_geom_frag_def(program, vert_shader, geom_shader, frag_shader, extra_defines) do { \
    program_add_shader(program, Vertex, vert_shader, extra_defines); \
    program_add_shader(program, Geometry, geom_shader, extra_defines); \
    program_add_shader(program, Fragment, frag_shader, extra_defines); \
    program_link(program); \
    } while(false)

#define program_vert_geom_frag(program, vert_shader, geom_shader, frag_shader) program_vert_geom_frag_def(program, vert_shader, geom_shader, frag_shader, Defines())


#define program_compute(program, comp_shader) do { \
    program_add_shader(program, Compute, comp_shader, Defines()); \
    program_link(program); \
    } while(false)

        program_vert_geom_frag(render_layers_program,
                               "render_layers.vert",
                               "render_layers.geom",
                               "forward.frag");

        program_vert_frag(blit_layer_program,
                          "fs.vert",
                          "blit_layer.frag");

        program_vert_frag(blit_program,
                          "fs.vert",
                          "blit_texture.frag");

        program_compute(copy_fragments_program,
                        "copy_fragments.comp");

        program_compute(combine_layers_program,
                        "dof.comp");
    }

    void renderLayers() {
        const mat4 M = mat4(1.0f);
        const mat3 N = inverse(transpose(M));

        camera.ratio = static_cast<float>(width) / static_cast<float>(height);
        camera.computeMatrices(&trackball, M, 0);

        glBindFramebuffer(GL_FRAMEBUFFER, layered_fbo);
        glViewport(0, 0, width, height);

        constexpr GLenum draw_buffers[] = {GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1};
        glDrawBuffers(2, draw_buffers);

        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glEnable(GL_DEPTH_TEST);
        glEnable(GL_CULL_FACE);

        const float depth_vs_clear[4] = {camera.camFar, 0.f, 0.f, 0.f};
        glClearTexImage(layered_depth_vs, 0, GL_RED, GL_FLOAT, depth_vs_clear);

        render_layers_program.bind();
        render_layers_program.UniformMatrix4fv("MV", 1, GL_FALSE, value_ptr(camera.matMV));
        render_layers_program.UniformMatrix4fv("P", 1, GL_FALSE, value_ptr(camera.matP));
        render_layers_program.UniformMatrix3fv("N", 1, GL_FALSE, value_ptr(N));
        render_layers_program.Uniform1i("num_layers", params.num_layers);
        render_layers_program.Uniform1f("near", camera.camNear);
        render_layers_program.Uniform1f("far", camera.camFar);
        this->scene->draw(&render_layers_program, RENDER_TEXTURES);

        glDisable(GL_CULL_FACE);
        glDisable(GL_DEPTH_TEST);
        glUseProgram(0);

        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        constexpr GLenum back_buffer[] = {GL_BACK};
        glDrawBuffers(1, back_buffer);
    }

    void copyFragments() {
        this->copy_fragments_program.bind();
        this->copy_fragments_program.Uniform1i("num_layers", params.num_layers);
        this->copy_fragments_program.Uniform1f("near", camera.camNear);
        this->copy_fragments_program.Uniform1f("far", camera.camFar);
        this->copy_fragments_program.Uniform1f("overlap", params.layer_overlap);

        glBindImageTexture(0, layered_color, 0, GL_TRUE, 0, GL_READ_WRITE, GL_RGBA8);
        glBindImageTexture(1, layered_depth_vs, 0, GL_TRUE, 0, GL_READ_WRITE, GL_R32F);

        glMemoryBarrier(GL_ALL_BARRIER_BITS);
        glDispatchCompute((this->width + 15) / 16, (this->height + 15) / 16, 1);

        glMemoryBarrier(GL_ALL_BARRIER_BITS);

        glUseProgram(0);
    }

    void combineLayers() {
        this->combine_layers_program.bind();
        this->combine_layers_program.Uniform1i("num_layers", params.num_layers);
        this->combine_layers_program.Uniform1f("near", camera.camNear);
        this->combine_layers_program.Uniform1f("far", camera.camFar);
        this->combine_layers_program.Uniform1f("focal_length", params.focal_length);
        this->combine_layers_program.Uniform1f("f_stop", params.f_stop);
        this->combine_layers_program.Uniform1f("d_f", params.d_f);
        this->combine_layers_program.Uniform1f("dof_strength", params.dof_strength);
        this->combine_layers_program.Uniform1i("dof_samples", params.dof_samples);

        glBindImageTexture(0, layered_color, 0, GL_TRUE, 0, GL_READ_ONLY, GL_RGBA8);
        glBindImageTexture(1, layered_depth_vs, 0, GL_TRUE, 0, GL_READ_ONLY, GL_R32F);
        glBindImageTexture(2, combined_image, 0, GL_TRUE, 0, GL_WRITE_ONLY, GL_RGBA8);

        glMemoryBarrier(GL_ALL_BARRIER_BITS);
        glDispatchCompute((this->width + 15) / 16, (this->height + 15) / 16, 1);
        glMemoryBarrier(GL_ALL_BARRIER_BITS);
        glUseProgram(0);
    }

    void blitLayer() {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        glViewport(0, 0, width, height);

        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glBindVertexArray(vao_empty);
        blit_layer_program.bind();
        blit_layer_program.Uniform1f("exposure", params.exposure);

        glActiveTexture(GL_TEXTURE0);
        if (params.show_depth_vs) {
            glBindTexture(GL_TEXTURE_2D_ARRAY, layered_depth_vs);
        } else {
            glBindTexture(GL_TEXTURE_2D_ARRAY, layered_color);
        }
        blit_layer_program.Uniform1i("layered_color", 0);
        blit_layer_program.Uniform1i("layer", params.layer_to_show);

        glDrawArrays(GL_TRIANGLES, 0, 3);

        glUseProgram(0);
    }

    void blit() {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        glViewport(0, 0, width, height);

        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glBindVertexArray(vao_empty);
        blit_program.bind();
        blit_program.Uniform1f("exposure", params.exposure);

        BINDTEX(blit_program, "color_tex", combined_image, GL_TEXTURE0);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        glUseProgram(0);
        glBindVertexArray(0);
    }

    void sceneRenderFrame(int invocation) override {
        static int prevLayerCount = params.num_layers;
        if (prevLayerCount != params.num_layers) {
            this->createFramebuffers();
            prevLayerCount = params.num_layers;
        }

        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        params.layer_to_show = std::clamp(params.layer_to_show, 0, params.num_layers - 1);

        renderLayers();
        if (params.copy_fragments) {
            this->copyFragments();
        }
        this->combineLayers();
        CheckErrorsGL();
        if (params.show_individual_layer) {
            blitLayer();
        } else {
            blit();
        }
    }
};

CRender *pRenderClass;


void window_size_callback(GLFWwindow *window, const int width, const int height) {
    if (window == glfwWindow && pRenderClass != nullptr) {
        pRenderClass->windowSizeChanged(width, height);
    }
}


void initialize() {
    pRenderClass = new CRender();
    glfwSetFramebufferSizeCallback(glfwWindow, window_size_callback);
}

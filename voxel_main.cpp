/*
________             _____      ________________________
    ___  __ \______________  /________  ____/__  /___  ____/
    __  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
    _  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
    /_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)
*/


#define USE_TWEAK_BAR

#include "stdafx.h"

char applicationTitle[128] = "Voxelize";

const char path2Demo[] = "Assignments/InCG-Voxel/";

using namespace glm;

TwBar* bar = NULL; // Pointer to a tweak bar

vec4 g_ObjectRotation = vec4(0, 0, 0, 1);
vec3 g_BackgroundColor = vec3(0.0f, 0.0f, 0.0f);

int g_Mode = 0, g_Progressive = 0;
float g_Exposure = 0.0f, g_Gamma = 1.0f;

float stepSize = 0.02;

struct Triangle {
    glm::vec3 a, b, c;
};

void initializeTweakBar() {
    if (bar != NULL)
        TwDeleteBar(bar);
    else
        TwTerminate();
    nTweakBarVariables = 0;

    // Create a tweak bar
    TwDefine("GLOBAL fontscaling=1");
    TwInit(TW_OPENGL, NULL);
    TwDefine("GLOBAL fontsize=3");

    bar = TwNewBar("DVR");

    TwDefine("'DVR' position='8 30'");
    TwDefine("'DVR' size='400 500'");
    TwDefine("'DVR' text=light");

    TwEnumVal mode[2] = {{0, "Voxels"}, {1, "Scene"}};
    TwType tm = TwDefineEnum("Mode", mode, 2);
    TwAddVarRW(bar, "Mode (m)", tm, &g_Mode, "  keyIncr='m' keyDecr='M' ");

    TwAddVarRW(bar, "progressive (p)", TW_TYPE_BOOL32, &g_Progressive, " keyIncr='p' label='Progressive Update'");
    TwAddVarRW(bar, "light", TW_TYPE_QUAT4F, (float*)&g_ObjectRotation, "");
    TwAddVarRW(bar, "background", TW_TYPE_COLOR3F, (float*)&g_BackgroundColor, "");

    TwAddVarRW(bar, "stepSize RM", TW_TYPE_FLOAT, &stepSize, " min=0.005 max=1.0 step=0.001 group='Parameters'");

    TwAddVarRW(bar, "exposure", TW_TYPE_FLOAT, &g_Exposure, " min=-4.0 max=4.0 step=0.01 group='Display'");
    TwAddVarRW(bar, "gamma", TW_TYPE_FLOAT, &g_Gamma, " min=1.0 max=3.0 step=0.01 group='Display'");
}


class CRender : public CRenderBase {
protected:
    Scene* scene;
    Scene* sceneVox;
    Scene* sceneMesh;
    Camera camera;
    GLSLProgram prgRenderDVR; // GLSL programs, each one can keep a vertex and a fragment shader
    GLSLProgram prgVoxelCone; // GLSL programs, each one can keep a vertex and a fragment shader
    GLSLProgram prgVoxelize;
    // OGLTexture* tVolume;
    GLuint voxels;

    // int sampleIdx;

    bool mouseUpdate;
    int lastMouseX, lastMouseY;
    float mouseXPos, mouseYPos;

    bool shaderUpdate;

    IMWrap wrap;
    uint8_t mouseButton;
    const char* defineString = NULL;

    // TODO change for second Task
    bool geometryShader = false;
    const int voxelDim = 64;

    std::vector<Triangle> tris;
    std::vector<uint32_t> vox = std::vector<uint32_t>(voxelDim * voxelDim * voxelDim);

    glm::vec3 aabbMin = glm::vec3(-1);
    glm::vec3 aabbMax = glm::vec3(1);

public:
    CRender() : mouseButton(0) {
        glfwGetWindowSize(glfwWindow, &width, &height);

        offScreenRenderTarget = !false; // required for multi sampling, stereo, accumulation
        useMultisampling = false;
        stereoRendering = false;
        useAccumulationBuffer = !false; // call clearAccumulationBuffer(); in sceneFrameRender() to clear the buffer
        enableGLDebugOutput = true;

        // called here as the initialization depends on some flags we can set in CRender
        CRenderBase::CRenderBaseInit();

        // load and/or create shaders, textures, and models
        loadShaders(true);
        loadModels();
        if (!geometryShader) {
            voxelize();
        }
        createTextures();


        // call it here so that these textures show up at the end in the texture manager
        CRenderBase::createTextures();
    }

    ~CRender() {
        if (scene) delete scene;
        if (sceneVox) delete sceneVox;
        if (sceneMesh) delete sceneMesh;
    }

    //
    // load 3d models
    //
    void loadModels() {
        scene = new Scene(texMan);
        sceneVox = new Scene(texMan);
        sceneMesh = new Scene(texMan);
        const char* attribs[3] = {"in_position", "in_normal", "in_texcoord"};
        mat4x4 matrix = rotate(mat4(1.0f), radians(-90.0f), vec3(1.0f, 0.0f, 0.0f));
        sceneVox->loadOBJ(SCENE_SMOOTH, prgRenderDVR.getProgramObject(), 3, (const char**)attribs, "box.obj", "./data/",
                          true, &matrix);
        scene->loadOBJ(SCENE_SMOOTH, prgVoxelCone.getProgramObject(), 3, (const char**)attribs, "horse.obj", "./data/",
                       true, &matrix);
        sceneMesh->loadOBJ(SCENE_SMOOTH, prgVoxelize.getProgramObject(), 3, (const char**)attribs, "horse.obj",
                           "./data/", true, &matrix);

        auto indices = this->scene->shapes[0].mesh.indices;
        auto positions = this->scene->shapes[0].mesh.positions;

        std::vector<glm::vec3> pos = std::vector<glm::vec3>(positions.size() / 3);
        for (int i = 0; i < positions.size() / 3; i++) {
            pos[i].x = positions[3 * i + 0];
            pos[i].y = positions[3 * i + 1];
            pos[i].z = positions[3 * i + 2];
        }

        tris = std::vector<Triangle>(indices.size() / 3);
        for (int i = 0; i < indices.size(); i += 3) {
            Triangle tri;
            tri.a = pos[indices[i]];
            tri.b = pos[indices[i + 1]];
            tri.c = pos[indices[i + 2]];

            tris[i / 3] = tri;
        }
    }

    //
    // load vertex and fragment shaders
    //
    void loadShaders(bool firstTime = false) {
#ifdef USE_TWEAK_BAR
        initializeTweakBar();
#endif

        if (!firstTime) CRenderBase::loadShaders(firstTime);

        // load and setup a shader
        if (!prgVoxelize.loadVertexShader(tmpStrCat(path2Demo, "shader/voxelize.vp.glsl"), defineString) ||
            !prgVoxelize.loadGeometryShader(tmpStrCat(path2Demo, "shader/voxelize.gs.glsl"), defineString) ||
            !prgVoxelize.loadFragmentShader(tmpStrCat(path2Demo, "shader/voxelize.fp.glsl"), defineString)) {
            if (firstTime) exit(1);
        }

        prgVoxelize.link();

        // load and setup a shader
        if (!prgRenderDVR.loadVertexShader(tmpStrCat(path2Demo, "shader/compute_pixel.vp.glsl"), defineString) ||
            !prgRenderDVR.loadFragmentShader(tmpStrCat(path2Demo, "shader/compute_pixel.fp.glsl"), defineString)) {
            if (firstTime) exit(1);
        }

        prgRenderDVR.link();
        glBindFragDataLocation(prgRenderDVR.getProgramObject(), 0, "out_color");

        if (!prgVoxelCone.loadVertexShader(tmpStrCat(path2Demo, "shader/voxel_cone.vp.glsl"), defineString) ||
            !prgVoxelCone.loadFragmentShader(tmpStrCat(path2Demo, "shader/voxel_cone.fp.glsl"), defineString)) {
            if (firstTime) exit(1);
        }
        prgVoxelCone.link();
        glBindFragDataLocation(prgVoxelCone.getProgramObject(), 0, "out_color");
    }

    //
    // create textures and render targets
    //
    void createTextures() {
        glGenTextures(1, &voxels);
        glBindTexture(GL_TEXTURE_3D, voxels);
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP);
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP);
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP);
        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA32F, voxelDim, voxelDim, voxelDim, 0, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8,
                     vox.data());
        glBindImageTexture(0, voxels, 0, GL_TRUE, 0, GL_READ_WRITE, GL_RGBA32F);
        glGenerateMipmap(GL_TEXTURE_3D);
    }

    bool mouseFunc(int button, int state, int x, int y, int mods) {
        if (button == GLFW_MOUSE_BUTTON_LEFT && state == GLFW_RELEASE) mouseButton &= ~1;
        if (button == GLFW_MOUSE_BUTTON_RIGHT && state == GLFW_RELEASE) mouseButton &= ~2;
        return CRenderBase::mouseFunc(button, state, x, y, mods);
    }

    bool mouseMotion(int x, int y) {
        mouseXPos = (float)x / (float)width;
        mouseYPos = (float)y / (float)height;
        if (lastMouseX != x || lastMouseY != y) {
            mouseUpdate = true;
            lastMouseX = x;
            lastMouseY = y;
        }

        return CRenderBase::mouseMotion(x, y);
    }

    glm::vec3 shiftInterval(glm::vec3  t, glm::vec3  a, glm::vec3  b, glm::vec3  c, glm::vec3  d) {
        return c + (d - c) / (b - a) * (t - a);
    }

    // triangle box intersection test
    void voxelize() {
        #pragma omp parallel
        {
#pragma omp for
            for (int i = 0; i < voxelDim * voxelDim * voxelDim; ++i) {
                int z = i / (voxelDim * voxelDim);
                int a = i - z * (voxelDim * voxelDim);
                int y = a / voxelDim;
                int x = a % voxelDim;
                glm::vec3 min(x, y, z);
                glm::vec3 max(x + 1, y + 1, z + 1);

                min = shiftInterval(min, glm::vec3(0), glm::vec3(voxelDim),aabbMin,aabbMax );
                max = shiftInterval(max, glm::vec3(0), glm::vec3(voxelDim),aabbMin,aabbMax );
                vox[i] = 255;
            }
        }
    }

    //
    // render a frame of the scene (multiple invocations possible for accumulation buffers or stereo-/multi-view-rendering; just ignore if not required)
    //
    void sceneRenderFrame(int invocation = 0) {
        // set some render states
        glEnable(GL_DEPTH_TEST);
        glEnable(GL_CULL_FACE);

        // clear screen
        glClearColor(g_BackgroundColor.x, g_BackgroundColor.y, g_BackgroundColor.z, 0.2f);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);


        if (useAccumulationBuffer && (trackball.hasUpdated() || shaderUpdate || !g_Progressive)) {
            clearAccumulationBuffer();
            shaderUpdate = false;
            mouseUpdate = false;
        }

        mat4 matM;
        camera.computeMatrices(&trackball, matM, 0);
        glm::quat quat = glm::quat(g_ObjectRotation.w, g_ObjectRotation.x, g_ObjectRotation.y, g_ObjectRotation.z);
        vec3 lightPos = normalize(glm::vec3((glm::toMat4(quat)[0])));

        // voxelize scene
        if (geometryShader) {
            glDisable(GL_CULL_FACE);
            prgVoxelize.bind();
            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_3D, voxels);
            prgVoxelize.UniformMatrix4fv((char*)"matM", 1, false, value_ptr(matM));
            prgVoxelize.UniformMatrix4fv((char*)"matMVP", 1, false, value_ptr(camera.matMVP));
            prgVoxelize.Uniform1i((char*)"numberOfLights", 1);
            prgVoxelize.Uniform3fv((char*)"pointLights[0].position", 1, value_ptr(lightPos));
            prgVoxelize.Uniform3fv((char*)"pointLights[0].color", 1, value_ptr(glm::vec3(1)));
            sceneMesh->draw(&prgVoxelize, 0);

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glEnable(GL_CULL_FACE);
        }

        if (g_Mode == 1) {
            prgVoxelCone.bind();
            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_3D, voxels);

            prgVoxelCone.UniformMatrix4fv((char*)"M", 1, false, value_ptr(matM));
            prgVoxelCone.UniformMatrix4fv((char*)"MVP", 1, false, value_ptr(camera.matMVP));
            prgVoxelCone.Uniform3fv((char*)"cameraPosition", 1, value_ptr(camera.camPos));
            prgVoxelCone.Uniform1i((char*)"numberOfLights", 1);
            prgVoxelCone.Uniform3fv((char*)"pointLights[0].position", 1, value_ptr(lightPos));
            prgVoxelCone.Uniform3fv((char*)"pointLights[0].color", 1, value_ptr(glm::vec3(1)));

            scene->draw(&prgVoxelCone, 0);
        }
        else {
            // now bind the program and set the parameters
            prgRenderDVR.bind();

            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_3D, voxels);

            prgRenderDVR.UniformMatrix4fv((char*)"matM", 1, false, value_ptr(matM));
            prgRenderDVR.UniformMatrix4fv((char*)"matMVP", 1, false, value_ptr(camera.matMVP));

            prgRenderDVR.Uniform3fv((char*)"camPos", 1, value_ptr(camera.camPos));
            prgRenderDVR.Uniform1f((char*)"rmStepSize", stepSize);

            // display widget
            sceneVox->draw(&prgRenderDVR, 0);
        }


        setExposureGamma(g_Exposure, g_Gamma);
    }
};

// no need to modify anything below this line

CRender* pRenderClass;

void initialize() {
    pRenderClass = new CRender();
}

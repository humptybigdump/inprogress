#ifndef __stdafx_h
#define __stdafx_h

#pragma warning ( disable : 4530 ) 

#define USE_TWEAK_BAR
//#define NON_MINIMAL_BUILD
#define USE_SCREEN_LENS
#define USE_ENVMAP
#define USE_OLD_GLM_OBJ
#define TEXTURE_MANAGER_GUI
#define SCREEN_BUILD_BVH
//#define USE_OPENGL_TEXT

#include <omp.h>

#define _USE_MATH_DEFINES
#define NOMINMAX
#if defined(_WIN32) || defined( WIN32 ) 
#include <windows.h>
#include <minmax.h>
#include <algorithm>
#endif
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>
#include <malloc.h>

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>


#define GLEW_STATIC
#include "GL/glew.h"
#if defined(_WIN32)
#  include "GL/wglew.h"
#elif !defined(__APPLE__) || defined(GLEW_APPLE_GLX)
#  include "GL/glxew.h"
#endif

#include "GLFW/glfw3.h"

#define GLM_FORCE_CXX98
//#define GLM_FORCE_PURE
//#define GLM_FORCE_AVX2
//#define GLM_FORCE_SSE42
//#define GLM_FORCE_INLINE
#include "glm/glm.hpp"
#include "glm/gtc/quaternion.hpp"

#include "glm/gtx/quaternion.hpp"
#include "glm/gtx/color_space.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtc/type_ptr.hpp"

#include "framebufferObject.h"
#include "renderbuffer.h"
#include "glErrorUtil.h"
#include "texture.h"
#include "buffer.h"
#include "GLSLProgram.h"
#include "IMWrapper.h"
#ifdef USE_OLD_GLM_OBJ
#include "glm.h"
#endif

#include "fileio.h"
#include "guifont.h"
#include "trackball.h"
#include "rgbe.h"
#include "texturemanager.h"
#include "RTWrapper.h"
#include "camera.h"

#ifdef USE_SCREEN_LENS
#include "lens.h"
#endif

#include "render.h"
#include "tiny_obj_loader.h"
#include "scene.h"

#ifdef USE_ENVMAP
#include "envmap.h"
#endif

#ifdef USE_OPENGL_TEXT
#include "OpenGLText.h"
#endif

#include "helpers.h"

#ifdef NON_MINIMAL_BUILD
#include "shapes.h"
#include "lean_mapping.h"
#include "ShadowMap.h"
#endif


#ifdef USE_TWEAK_BAR
#include <AntTweakBar.h>
#include "tweakBarGLSLUniforms.h"
#endif

extern int mainProtoGLF( int argc, char **argv );

#endif

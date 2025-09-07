/*
    ________             _____      ________________________
    ___  __ \______________  /________  ____/__  /___  ____/
    __  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
    _  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
    /_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ scene class for loading OBJs and proving data to the renderer
*/

#ifndef __SCENE_H
#define __SCENE_H

#define SCENE_FLAT				0x01
#define SCENE_SMOOTH			0x02
#define SCENE_TEXTURE			0x04
#define SCENE_COLOR				0x08
#define SCENE_AMBIENT_OCCLUSION 0x10
#define SCENE_BENT_NORMAL		0x20

#define RENDER_TEXTURES			0x01
#define RENDER_MATERIALS		0x02

#include <chrono>
#include <stdint.h>

#include "stdafx.h"
#ifdef SCREEN_BUILD_BVH
#include "accelerator2.h"
#endif

using namespace std;
using namespace glm;

class Scene {
public:
    TextureManager* texMan;

    int nShapes;
    std::vector<tinyobj::shape_t> shapes;
    std::vector<IMWrap *> wrapper;
    std::vector<OGLTexture *> mapKa;
    std::vector<OGLTexture *> mapKd;
    std::vector<OGLTexture *> mapKs;
    std::vector<OGLTexture *> mapNs;

    OGLTexture* tDummy,* tDummyNrml;

#ifdef SCREEN_BUILD_BVH
    char bvhCacheFile[ 8192 ], _basePath[ 8192 ];
    bool rebuildBVH;

    BVHAcceleratorLinear* bvh;

    // for uploading the BVH to GPU (+ random numbers)
    GLuint csLinearBVH, csLinearTriangles, csLinearTriangleData, csMaterialList, csLightList;
    GLuint csRandom;
    GLuint csFrame, csNMaterials, csNLights;

    float* csImage;
    float* csRandomNumbers;

    int nBVHTextures;
    std::vector<char *> mapBVHFilename;
    std::vector<OGLTexture *> mapBVH;
#endif

public:
    void drawShape(int i, GLSLProgram* program, int mode) {
        if (mode & RENDER_TEXTURES) // set textures
        {
            float fLargest;
            glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, &fLargest);
            fLargest = 1.0f;

            glActiveTexture(GL_TEXTURE3_ARB);
            mapNs[i]->bind();
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
            glActiveTexture(GL_TEXTURE2_ARB);
            mapKs[i]->bind();
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
            glActiveTexture(GL_TEXTURE1_ARB);
            mapKd[i]->bind();
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
            glActiveTexture(GL_TEXTURE0_ARB);
            mapKa[i]->bind();
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);

            program->Uniform1i((char *) "tObjMapKa", 0);
            program->Uniform1i((char *) "tObjMapKd", 1);
            program->Uniform1i((char *) "tObjMapKs", 2);
            program->Uniform1i((char *) "tObjMapNs", 3);
        }
        if (mode & RENDER_MATERIALS) // set materials
        {
            program->Uniform3fv("objMatAmbient", 1, &shapes[i].material.ambient[0]);
            program->Uniform3fv("objMatDiffuse", 1, &shapes[i].material.diffuse[0]);
            program->Uniform3fv("objMatSpecular", 1, &shapes[i].material.specular[0]);
            program->Uniform3fv("objMatEmission", 1, &shapes[i].material.emission[0]);
            program->Uniform1f("objMatShininess", shapes[i].material.shininess);
        }

        wrapper[i]->draw();
    }

    void draw(GLSLProgram* program, int mode) {
        for (int i = 0; i < nShapes; i++) {
            if (mode & RENDER_TEXTURES) // set textures
            {
                float fLargest;
                glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, &fLargest);
                fLargest = 1.0f;

                glActiveTexture(GL_TEXTURE3_ARB);
                mapNs[i]->bind();
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
                glActiveTexture(GL_TEXTURE2_ARB);
                mapKs[i]->bind();
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
                glActiveTexture(GL_TEXTURE1_ARB);
                mapKd[i]->bind();
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);
                glActiveTexture(GL_TEXTURE0_ARB);
                mapKa[i]->bind();
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, fLargest);

                program->Uniform1i((char *) "tObjMapKa", 0);
                program->Uniform1i((char *) "tObjMapKd", 1);
                program->Uniform1i((char *) "tObjMapKs", 2);
                program->Uniform1i((char *) "tObjMapNs", 3);
            }
            if (mode & RENDER_MATERIALS) // set materials
            {
                program->Uniform3fv("objMatAmbient", 1, &shapes[i].material.ambient[0]);
                program->Uniform3fv("objMatDiffuse", 1, &shapes[i].material.diffuse[0]);
                program->Uniform3fv("objMatSpecular", 1, &shapes[i].material.specular[0]);
                program->Uniform3fv("objMatEmission", 1, &shapes[i].material.emission[0]);
                program->Uniform1f("objMatShininess", shapes[i].material.shininess);
            }

            wrapper[i]->draw();
        }
    }

    void exportOBJ(const char* filename) {
    }

    bool loadOBJ(int mode, const GLhandleARB shader, int _nAttribs, const char** names, const char* filename,
                 const char* basepath, bool bNormalize = true, mat4x4* transform = NULL) {

        char buf[ 8192 ];
        sprintf(buf, "%s%s", basepath, filename);

        _FILEIO f;
        
        // compute simple checksum of input file
        uint16_t crc = 0xFFFF;
        if ( f.readFile( buf ) )
        {
            f.seek( 0, SEEK_END );
            int l = f.tell();
            f.seek( 0, SEEK_SET );
            unsigned char *tmp = new unsigned char[ l ];
            f.get( tmp, l );

            unsigned char *p = tmp;
            while ( l-- )
            {
                unsigned char x = crc >> 8 ^ *p++;
                x ^= x >> 4;
                crc = ( crc << 8 ) ^ ( (uint16_t)( x << 12 ) ) ^ ( (uint16_t)( x << 5 ) ) ^ ( (uint16_t)x );
            }
            f.closeFile();
        } else
        {
            printf( " [OBJ]: error loading %s ...\n", filename );
            exit( 1 );
        }
        
        char bufOut[ 8192 ];
        sprintf( bufOut, "%s%s.3d", basepath, filename );

        strcpy( _basePath, basepath );
        sprintf( bvhCacheFile, "%s%s.bvh", basepath, filename );

        bool readCached = f.readFile(bufOut);

        rebuildBVH = false;
        if ( readCached )
        {
            unsigned short cachedCRC = f.getU16();
            if ( cachedCRC != crc )
            {
                readCached = false;
                rebuildBVH = true;
                f.closeFile();
            }
        }

        int nShapesLoaded = 0;
        std::vector<tinyobj::shape_t> tshapes;

        if (!readCached) {
            printf(" [OBJ]: loading %s ...\n", filename);
            std::string err = tinyobj::LoadObj(tshapes, (std::string(basepath) + "/" + filename).c_str(), basepath);

            if (!err.empty()) {
                std::cerr << err << std::endl;
                return false;
            }

            printf(" [OBJ]: preprocessing and wrapping ...\n");
            // mesh preprocessing
            vec3 aabbMin = vec3(1e37f), aabbMax = vec3(-1e37f);

            if (bNormalize)
                for (size_t i = 0; i < tshapes.size(); i++) {
                    for (size_t v = 0; v < tshapes[i].mesh.positions.size(); v += 3) {
                        aabbMax = max(aabbMax, *((vec3 *) &tshapes[i].mesh.positions[v]));
                        aabbMin = min(aabbMin, *((vec3 *) &tshapes[i].mesh.positions[v]));
                    }
                }

            vec3 translate = -0.5f * (aabbMax + aabbMin);
            vec3 ext = aabbMax - aabbMin;
            float scale = 1.0f / std::max(ext.x, std::max(ext.y, ext.z));

            mat4x4 matNrml = mat4x4(1.0f);
            if (transform != NULL) {
                matNrml = transpose(inverse(*transform));

                for (size_t i = 0; i < tshapes.size(); i++) {
                    for (size_t v = 0; v < tshapes[i].mesh.normals.size(); v += 3) {
                        vec4 p = matNrml * vec4(*((vec3 *) &tshapes[i].mesh.normals[v]), 0.0f);

                        *((vec3 *) &tshapes[i].mesh.normals[v]) = normalize(vec3(p));
                    }
                }
            }

            if (bNormalize || transform != NULL)
                for (size_t i = 0; i < tshapes.size(); i++) {
                    for (size_t v = 0; v < tshapes[i].mesh.positions.size(); v += 3) {
                        vec3 x = *((vec3 *) &tshapes[i].mesh.positions[v]);

                        if (bNormalize)
                            x = (x + translate) * scale;

                        if (transform != NULL) {
                            vec4 p = *transform * vec4(x, 1.0f);
                            x = vec3(p) / p.w;
                        }

                        *((vec3 *) &tshapes[i].mesh.positions[v]) = x;
                    }
                }

#ifdef SCREEN_BUILD_BVH
            if ( mode & SCENE_AMBIENT_OCCLUSION || mode & SCENE_BENT_NORMAL ) {
                // removed for now
            }
#endif

            nShapesLoaded = (int) tshapes.size();

            f.writeFile(bufOut);
            f.putU16( crc );
            f.putU32(nShapesLoaded);
            for (size_t i = 0; i < nShapesLoaded; i++) {
                // object name
                f.putString(tshapes[i].name.c_str());

                // material
                f.putString(tshapes[i].material.name.c_str());
                f.putF3(&tshapes[i].material.ambient[0]);
                f.putF3(&tshapes[i].material.diffuse[0]);
                f.putF3(&tshapes[i].material.specular[0]);
                f.putF3(&tshapes[i].material.transmittance[0]);
                f.putF3(&tshapes[i].material.emission[0]);
                f.putF32(tshapes[i].material.shininess);
                f.putF32(tshapes[i].material.ior);
                f.putF32(tshapes[i].material.dissolve);
                f.putS32(tshapes[i].material.illum);
                f.putString(tshapes[i].material.ambient_texname.c_str());
                f.putString(tshapes[i].material.diffuse_texname.c_str());
                f.putString(tshapes[i].material.specular_texname.c_str());
                f.putString(tshapes[i].material.normal_texname.c_str());

                // mesh
                f.putU32((unsigned int) tshapes[i].mesh.positions.size());
                for (unsigned int j = 0; j < tshapes[i].mesh.positions.size(); j++)
                    f.putF32(tshapes[i].mesh.positions[j]);

                f.putU32((unsigned int) tshapes[i].mesh.normals.size());
                for (unsigned int j = 0; j < tshapes[i].mesh.normals.size(); j++)
                    f.putF32(tshapes[i].mesh.normals[j]);

                f.putU32((unsigned int) tshapes[i].mesh.texcoords.size());
                for (unsigned int j = 0; j < tshapes[i].mesh.texcoords.size(); j++)
                    f.putF32(tshapes[i].mesh.texcoords[j]);

                f.putU32((unsigned int) tshapes[i].mesh.ao.size());
                for (unsigned int j = 0; j < tshapes[i].mesh.ao.size(); j++)
                    f.putF32(tshapes[i].mesh.ao[j]);

                f.putU32((unsigned int) tshapes[i].mesh.indices.size());
                for (unsigned int j = 0; j < tshapes[i].mesh.indices.size(); j++)
                    f.putU32(tshapes[i].mesh.indices[j]);
            }
            f.closeFile();
        } else {
            printf(" [OBJ]: loading cached binary %s.3d ...\n", filename);

            nShapesLoaded = f.getU32();
            tshapes.clear();
            tshapes.resize(nShapesLoaded);

            for (size_t i = 0; i < nShapesLoaded; i++) {
                char temp[1024];
                // object name
                f.getString(temp, 1024);
                tshapes[i].name = std::string(temp);

                // material
                f.getString(temp, 1024);
                tshapes[i].material.name = temp;
                f.getF3(&tshapes[i].material.ambient[0]);
                f.getF3(&tshapes[i].material.diffuse[0]);
                f.getF3(&tshapes[i].material.specular[0]);
                f.getF3(&tshapes[i].material.transmittance[0]);
                f.getF3(&tshapes[i].material.emission[0]);
                tshapes[i].material.shininess = f.getF32();
                tshapes[i].material.ior = f.getF32();
                tshapes[i].material.dissolve = f.getF32();
                tshapes[i].material.illum = f.getS32();

                f.getString(temp, 1024);
                tshapes[i].material.ambient_texname = temp;
                f.getString(temp, 1024);
                tshapes[i].material.diffuse_texname = temp;
                f.getString(temp, 1024);
                tshapes[i].material.specular_texname = temp;
                f.getString(temp, 1024);
                tshapes[i].material.normal_texname = temp;

                // mesh
                int t = f.getU32();
                tshapes[i].mesh.positions.clear();
                for (int j = 0; j < t; j++)
                    tshapes[i].mesh.positions.push_back(f.getF32());

                t = f.getU32();
                tshapes[i].mesh.normals.clear();
                for (int j = 0; j < t; j++)
                    tshapes[i].mesh.normals.push_back(f.getF32());

                t = f.getU32();
                tshapes[i].mesh.texcoords.clear();
                for (int j = 0; j < t; j++)
                    tshapes[i].mesh.texcoords.push_back(f.getF32());

                t = f.getU32();
                tshapes[i].mesh.ao.clear();
                for (int j = 0; j < t; j++)
                    tshapes[i].mesh.ao.push_back(f.getF32());

                t = f.getU32();
                tshapes[i].mesh.indices.clear();
                for (int j = 0; j < t; j++)
                    tshapes[i].mesh.indices.push_back(f.getU32());
            }
            f.closeFile();
        }

        for (size_t i = 0; i < nShapesLoaded; i++) {
            shapes.push_back(tshapes[i]);

            tinyobj::shape_t* shape = &shapes[shapes.size() - 1];

            // load textures (if any)
            OGLTexture* map;

            if (mode & SCENE_TEXTURE) {
                if (strlen(shape->material.ambient_texname.c_str()) > 0) {
                    sprintf(buf, "%s%s", basepath, shape->material.ambient_texname.c_str());
                    texMan->CreateTextureFromTGA(&map, buf);
                    mapKa.push_back(map);
                } else
                    mapKa.push_back(tDummy);
                if (strlen(shape->material.diffuse_texname.c_str()) > 0) {
                    sprintf(buf, "%s%s", basepath, shape->material.diffuse_texname.c_str());
                    texMan->CreateTextureFromTGA(&map, buf);
                    mapKd.push_back(map);
                } else
                    mapKd.push_back(tDummy);
                if (strlen(shape->material.specular_texname.c_str()) > 0) {
                    sprintf(buf, "%s%s", basepath, shape->material.specular_texname.c_str());
                    texMan->CreateTextureFromTGA(&map, buf);
                    mapKs.push_back(map);
                } else
                    mapKs.push_back(tDummy);
                if (strlen(shape->material.normal_texname.c_str()) > 0) {
                    sprintf(buf, "%s%s", basepath, shape->material.normal_texname.c_str());
                    texMan->CreateTextureFromTGA(&map, buf);
                    mapNs.push_back(map);
                } else
                    mapNs.push_back(tDummyNrml);
            }

            // build wrapper

            int idxNrml = 0;
            int idxTexCoord = 0;
            int idxColor = 0;

            if (mode & SCENE_FLAT) {
                idxNrml = 1;
            }

            if (mode & SCENE_SMOOTH) {
                if (shape->mesh.normals.size() > 0) {
                    idxNrml = 1;
                } else {
                    printf(" [OBJ]: no normals for wrapper -- stopping!\n");
                    return false;
                }
            }

            if (mode & SCENE_TEXTURE) {
                if (shape->mesh.texcoords.size() > 0) {
                    idxTexCoord = idxNrml + 1;
                } else {
                    printf(" [OBJ]: no texcoords for wrapper -- stopping!\n");
                    return false;
                }
            }

            if (mode & SCENE_COLOR) {
                if (idxNrml && idxTexCoord)
                    idxColor = 3;
                else if (idxNrml || idxTexCoord)
                    idxColor = 2;
                else idxColor = 1;
            }

            // build wrapper
#define VTX2( k ) ( *( (vec3*)&shape->mesh.positions[ 3 * shape->mesh.indices[f+(k)] + 0 ] ) )
#define NRM( k ) ( *( (vec3*)&shape->mesh.normals[ 3 * shape->mesh.indices[f+(k)] + 0 ] ) )
#define TEX( k ) ( *( (vec3*)&shape->mesh.texcoords[ 2 * shape->mesh.indices[f+(k)] + 0 ] ) )

            IMWrap* wrap = new IMWrap();
            wrap->bindShaderAttribs(shader, _nAttribs, names);

            wrap->Begin(GL_TRIANGLES);
            for (size_t f = 0; f < shape->mesh.indices.size(); f += 3) {
                vec3 faceNrml;
                if (mode & SCENE_FLAT)
                    faceNrml = normalize(cross(VTX2(1) - VTX2(0), VTX2(2) - VTX2(0)));

                for (int j = 0; j < 3; j++) {
                    if (mode & SCENE_AMBIENT_OCCLUSION) {
                        float aoVal = 1.0f;
                        if (shape->mesh.ao.size() > 0)
                            aoVal = shape->mesh.ao[shape->mesh.indices[f + j]];

                        if (mode & SCENE_FLAT)
                            wrap->Attrib4f(idxNrml, faceNrml.x, faceNrml.y, faceNrml.z, aoVal);

                        if (mode & SCENE_SMOOTH)
                            wrap->Attrib4f(idxNrml, NRM(j).x, NRM(j).y, NRM(j).z, aoVal);
                    } else {
                        if (mode & SCENE_FLAT)
                            wrap->Attrib3f(idxNrml, faceNrml.x, faceNrml.y, faceNrml.z);

                        if (mode & SCENE_SMOOTH)
                            wrap->Attrib3fv(idxNrml, value_ptr(NRM(j)));
                    }

                    if (mode & SCENE_COLOR)
                        wrap->Attrib3fv(idxColor, &shape->material.diffuse[0]);

                    if (mode & SCENE_TEXTURE)
                        wrap->Attrib2fv(idxTexCoord, value_ptr(TEX(j)));

                    int test = shape->mesh.indices[f + j];
                    vec3 bla = VTX2(j);
                    wrap->Attrib3fv(0, value_ptr(bla));
                    wrap->emitVertex();
                }
            }
            wrap->End();

            wrapper.push_back(wrap);

            nShapes++;
        }

        return true;
    }

    float luminance(const vec3& c) {
        const float YWeight[3] = {0.212671f, 0.715160f, 0.072169f};
        return YWeight[0] * c.x + YWeight[1] * c.y + YWeight[2] * c.z;
    }

#ifdef SCREEN_BUILD_BVH
    bool buildBVH( int mode ) {
        FILE* f = NULL;

        //if (bvhFile != NULL)
        if ( !rebuildBVH )
            f = fopen(bvhCacheFile, "rb");

        nBVHTextures = 0;
        if (f != NULL) {
            bvh = new BVHAcceleratorLinear();
            printf("[SCNE]: reading %s...\n\n", bvhCacheFile );
            fread(&bvh->nLinearNodes, sizeof(unsigned int), 1, f);
            fread(&bvh->nLinearTriangles, sizeof(unsigned int), 1, f);
            bvh->linearBVH = new LinearBVHNode[bvh->nLinearNodes];
            bvh->linearTriangles = new LinearTriangle[bvh->nLinearTriangles];
            bvh->linearTriangleData = new LinearTriangleData[bvh->nLinearTriangles];
            fread(bvh->linearBVH, sizeof(LinearBVHNode), bvh->nLinearNodes, f);
            fread(bvh->linearTriangles, sizeof(LinearTriangle), bvh->nLinearTriangles, f);
            fread(bvh->linearTriangleData, sizeof(LinearTriangleData), bvh->nLinearTriangles, f);
            fread(&bvh->nMaterials, sizeof(unsigned int), 1, f);
            fread(bvh->matList, sizeof(Material), bvh->nMaterials, f);
            fread(&bvh->nLights, sizeof(unsigned int), 1, f);
            fread(bvh->lightList, sizeof(Light), bvh->nLights, f);

            fread(&nBVHTextures, sizeof(unsigned int), 1, f);

            mapBVH.clear();
            for (int i = 0; i < nBVHTextures; i++) {
                OGLTexture* map = NULL;
                char fn[1024], buf[2048];
                int p = 0;
                memset(fn, 0, 1024);
                do {
                    fread(&fn[p], 1, 1, f);
                    p++;
                } while (fn[p - 1] != 0);

                sprintf(buf, "%s%s", _basePath, fn);
                texMan->CreateTextureFromTGA(&map, buf);
                mapBVH.push_back(map);
            }

            fclose(f);
        } else {
            printf("[SCNE]: building BVH...\n");
            bvh = new BVHAcceleratorLinear();

            // material list
            bvh->nMaterials = 0;
            for (int i = 0; i < nShapes; i++) {
                memset(bvh->matList[i].data, 0, sizeof(float) * 16);
                *(unsigned int *) &(bvh->matList[i].data[14]) = 0xff;


                if (shapes[i].material.diffuse_texname.length() > 0) {
                    // check if the same texture has already been loaded
                    bool foundTexture = false;
                    for (int j = 0; j < i; j++) {
                        if (shapes[j].material.diffuse_texname.length() > 0)
                            if (strcmp(shapes[i].material.diffuse_texname.c_str(),
                                       shapes[j].material.diffuse_texname.c_str()) == 0) {
                                *(unsigned int *) &(bvh->matList[i].data[14]) = *(unsigned int *) &(bvh->matList[j].data
                                    [14]);
                                foundTexture = true;
                                break;
                            }
                    }

                    if (foundTexture)
                        goto reuseTextureButCopyMaterialData;

                    *(unsigned int *) &(bvh->matList[i].data[14]) = nBVHTextures;

                    char* n = new char[shapes[i].material.diffuse_texname.length() + 1];
                    strcpy(n, shapes[i].material.diffuse_texname.c_str());
                    mapBVHFilename.push_back(n);

                    OGLTexture* map;
                    char buf[2048];
                    sprintf(buf, "%s%s", _basePath, n);
                    if (texMan->CreateTextureFromTGA(&map, buf))
                        mapBVH.push_back(map);
                    else
                        mapBVH.push_back(tDummy);

                    nBVHTextures++;
                }
            reuseTextureButCopyMaterialData:

                char bla[1024];
                strcpy(bla, shapes[i].material.name.c_str());
                if (strstr(shapes[i].material.name.c_str(), "glass") != NULL) {
                    *(unsigned int *) &(bvh->matList[i].data[15]) = 1;

                    vec3 kt(0.2f, 0.2f, 0.2f), kr(0.64f, 0.72f, 0.8f);

                    kr = vec3(1.0f);
                    kt = vec3(1.0f);
                    float ior = 1.3f;

                    vec3 d = vec3(shapes[i].material.diffuse[0], shapes[i].material.diffuse[1],
                                  shapes[i].material.diffuse[2]);
                    vec3 s = vec3(shapes[i].material.specular[0], shapes[i].material.specular[1],
                                  shapes[i].material.specular[2]);

                    bvh->matList[i].data[0] = 0.5f;
                    bvh->matList[i].data[1] = d.x;
                    bvh->matList[i].data[2] = d.y;
                    bvh->matList[i].data[3] = d.z;

                    bvh->matList[i].data[4] = 0.5f;
                    bvh->matList[i].data[5] = kt.x;
                    bvh->matList[i].data[6] = kt.y;
                    bvh->matList[i].data[7] = kt.z;

                    bvh->matList[i].data[8] = ior;
                } else {
                    *(unsigned int *) &(bvh->matList[i].data[15]) = 0;

                    float kd, ks;
                    vec3 d = vec3(shapes[i].material.diffuse[0], shapes[i].material.diffuse[1],
                                  shapes[i].material.diffuse[2]);
                    vec3 s = vec3(shapes[i].material.specular[0], shapes[i].material.specular[1],
                                  shapes[i].material.specular[2]);

                    kd = luminance(d);
                    ks = luminance(s);

                    if (kd < 1e-7f && ks < 1e-7f) {
                        d = vec3(0.1f, 0.1f, 0.1f);
                        kd = luminance(d);
                    }
                    bvh->matList[i].data[0] = kd;
                    bvh->matList[i].data[1] = d.x;
                    bvh->matList[i].data[2] = d.y;
                    bvh->matList[i].data[3] = d.z;

                    bvh->matList[i].data[4] = ks;
                    bvh->matList[i].data[5] = s.x;
                    bvh->matList[i].data[6] = s.y;
                    bvh->matList[i].data[7] = s.z;
                    bvh->matList[i].data[8] = std::max(
                        100.0f, std::min(1.0f, shapes[i].material.shininess / 128.0f * 1000.0f));
                }

                bvh->nMaterials++;
            }

            unsigned int nTrianglesTotal = 0;
            for (int i = 0; i < nShapes; i++)
                nTrianglesTotal += (int) shapes[i].mesh.indices.size() / 3;


            TriangleL* objects = new TriangleL[nTrianglesTotal];
            int nTriangles = 0;

            // build wrapper
#define VTX3( k ) ( *( (vec3*)&shapes[ i ].mesh.positions[ 3 * shapes[ i ].mesh.indices[f+(k)] + 0 ] ) )
#define NRM3( k ) ( *( (vec3*)&shapes[ i ].mesh.normals  [ 3 * shapes[ i ].mesh.indices[f+(k)] + 0 ] ) )
#define TEX3( k ) ( *( (vec3*)&shapes[ i ].mesh.texcoords[ 2 * shapes[ i ].mesh.indices[f+(k)] + 0 ] ) )

            for (int i = 0; i < nShapes; i++)
                for (unsigned int f = 0; f < shapes[i].mesh.indices.size(); f += 3) {
                    TriangleL t;
                    t.a = VTX3(0);
                    t.b = VTX3(1);
                    t.c = VTX3(2);

                    t.n1 = NRM3(0);
                    t.n2 = NRM3(1);
                    t.n3 = NRM3(2);

                    if (shapes[i].mesh.texcoords.size() > 0) {
                        t.uv[0] = TEX3(0).x;
                        t.uv[1] = TEX3(0).y;
                        t.uv[2] = TEX3(1).x;
                        t.uv[3] = TEX3(1).y;
                        t.uv[4] = TEX3(2).x;
                        t.uv[5] = TEX3(2).y;
                    }

                    t.e1 = t.b - t.a;
                    t.e2 = t.c - t.a;
                    t.n = cross(t.e1, t.e2);
                    t.area = 0.5f * length(t.n);
                    t.n = normalize(t.n);

                    t.mat = i;

                    objects[nTriangles++] = t;
                }

            std::chrono::time_point<std::chrono::system_clock> t1 = std::chrono::system_clock::now();
            bvh->build(objects, nTriangles);
            std::chrono::time_point<std::chrono::system_clock> t2 = std::chrono::system_clock::now();

            glm::int64_t time = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();

            printf(" [BVH]: %Id milliseconds\n\n", time );

            // cache resulting BVH in binary/raw format
            if ( bvhCacheFile != NULL) {
                FILE* f = fopen( bvhCacheFile, "wb");
                fwrite(&bvh->nLinearNodes, sizeof(unsigned int), 1, f);
                fwrite(&bvh->nLinearTriangles, sizeof(unsigned int), 1, f);
                fwrite(bvh->linearBVH, sizeof(LinearBVHNode), bvh->nLinearNodes, f);
                fwrite(bvh->linearTriangles, sizeof(LinearTriangle), bvh->nLinearTriangles, f);
                fwrite(bvh->linearTriangleData, sizeof(LinearTriangleData), bvh->nLinearTriangles, f);
                fwrite(&bvh->nMaterials, sizeof(unsigned int), 1, f);
                fwrite(bvh->matList, sizeof(Material), bvh->nMaterials, f);
                fwrite(&bvh->nLights, sizeof(unsigned int), 1, f);
                fwrite(bvh->lightList, sizeof(Light), bvh->nLights, f);

                // textures
                fwrite(&nBVHTextures, sizeof(unsigned int), 1, f);
                for (int i = 0; i < nBVHTextures; i++)
                    fwrite(mapBVHFilename[i], strlen(mapBVHFilename[i]) + 1, 1, f);

                fclose(f);
            }
        }
        return true;
    }

    GLuint createShaderStorageBuffer(int size, GLenum usage = GL_STATIC_DRAW) {
        GLuint name;
        glGenBuffers(1, &name);
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, name);
        glBufferData(GL_SHADER_STORAGE_BUFFER, size, NULL, usage);
        //glBufferStorage( GL_SHADER_STORAGE_BUFFER, size, NULL, GL_MAP_WRITE_BIT);
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0);
        return name;
    }

    void copyMem2StorageBuffer(GLuint name, void* data, int size) {
        //GLint *ptr;
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, name);
        glBufferData(GL_SHADER_STORAGE_BUFFER, size, data, GL_DYNAMIC_DRAW);
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0);
    }

    void uploadBVH2GPU(int w, int h) {
        csImage = new float[w * h * 4];

        csRandom = createShaderStorageBuffer(sizeof(float) * 1024 * 1024 * 2);
        csRandomNumbers = new float[1024 * 1024 * 2];
        for (int i = 0; i < 1024 * 1024 * 2; i++)
            csRandomNumbers[i] = rand() / 32767.0f;

        csLinearBVH = createShaderStorageBuffer(sizeof(LinearBVHNode) * bvh->nLinearNodes);
        copyMem2StorageBuffer(csLinearBVH, bvh->linearBVH, sizeof(LinearBVHNode) * bvh->nLinearNodes);

        csLinearTriangles = createShaderStorageBuffer(sizeof(LinearTriangle) * bvh->nLinearTriangles);
        copyMem2StorageBuffer(csLinearTriangles, bvh->linearTriangles, sizeof(LinearTriangle) * bvh->nLinearTriangles);

        csLinearTriangleData = createShaderStorageBuffer(sizeof(LinearTriangleData) * bvh->nLinearTriangles);

        copyMem2StorageBuffer(csLinearTriangleData, bvh->linearTriangleData,
                              sizeof(LinearTriangleData) * bvh->nLinearTriangles);

        float* temp = new float[bvh->nMaterials * 16];
        float* ptr = temp;
        for (int i = 0; i < bvh->nMaterials; i++)
            for (int j = 0; j < 16; j++)
                *(ptr++) = bvh->matList[i].data[j];

        csMaterialList = createShaderStorageBuffer(sizeof(float) * bvh->nMaterials * 16);
        copyMem2StorageBuffer(csMaterialList, temp, sizeof(float) * bvh->nMaterials * 16);
        delete [] temp;

        if (bvh->nLights > 0) {
            csLightList = createShaderStorageBuffer(sizeof(Light) * bvh->nLights * 2);
            copyMem2StorageBuffer(csLightList, bvh->lightList, sizeof(Light) * bvh->nLights);
        }

        csRandom = createShaderStorageBuffer(sizeof(float) * 1024 * 1024 * 2);
        copyMem2StorageBuffer(csRandom, csRandomNumbers, sizeof(float) * 1024 * 1024 * 2);
    }

    void setBVHShaderUniforms(GLSLProgram* prg) {
        prg->bind();
        prg->Uniform1i("nMaterials", bvh->nMaterials);
        prg->Uniform1i("nLights", bvh->nLights);

        unsigned int textures[32];
        int n = std::min(32, (int) mapBVH.size());
        for (int i = 0; i < n; i++) {
            textures[i] = i;
            if (mapBVH[i] != NULL)
                mapBVH[i]->bind(GL_TEXTURE0 + i);
        }
        if (n)
            prg->Uniform1iv("tBVHTexture", n, (GLint *) &textures[0]);

        GLint block_index;
        GLuint binding_point_index;

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK, "blinearBVH");
        binding_point_index = 0;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, binding_point_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csLinearBVH);

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK, "blinearTriangles");
        binding_point_index = 1;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, binding_point_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csLinearTriangles);

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK, "bRandomNumbers");
        binding_point_index = 5;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, binding_point_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csRandom);

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK, "bmatList");
        binding_point_index = 3;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, block_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csMaterialList);

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK, "blightList");
        binding_point_index = 4;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, block_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csLightList);

        block_index = glGetProgramResourceIndex(prg->getProgramObject(), GL_SHADER_STORAGE_BLOCK,
                                                "blinearTriangleData");
        binding_point_index = 2;
        glShaderStorageBlockBinding(prg->getProgramObject(), block_index, binding_point_index);
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_point_index, csLinearTriangleData);
    }
#endif

    Scene(TextureManager* _texMan) {
        texMan = _texMan;

        unsigned int dummyPixel = 0x00FFFFFF, dummyNrml = 0x00FF0000;
        texMan->CreateTexture2D(&tDummy, 1, 1, GL_RGBA, GL_RGBA, GL_UNSIGNED_BYTE, &dummyPixel, "dummyTex", false);
        tDummy->bind();
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

        texMan->CreateTexture2D(&tDummyNrml, 1, 1, GL_RGBA, GL_RGBA, GL_UNSIGNED_BYTE, &dummyNrml, "dummyNrml", false);
        tDummyNrml->bind();
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

        nShapes = 0;
    };

    ~Scene() {
    };
};

#endif

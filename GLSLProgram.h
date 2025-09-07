/*
    ________             _____      ________________________
    ___  __ \______________  /________  ____/__  /___  ____/
    __  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
    _  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
    /_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ simple handling of GLSL shaders and programs
*/

#include "stdafx.h"
#pragma once

#include <filesystem>
#include <regex>

#pragma warning ( disable : 4996 )

#define SH_TYPE_UINT32	0x01
#define SH_TYPE_INT32	0x02
#define SH_TYPE_FLOAT	0x03
#define SH_TYPE_BOOL32	0x04

#define BINDTEX( ___prg, ___uniform, ___texture, ___unit ) \
		glBindMultiTextureEXT( ___unit, GL_TEXTURE_2D, ___texture );  \
		___prg.Uniform1i( (char*)(___uniform), ___unit - GL_TEXTURE0 );

#define BINDOGLTEX( ___prg, ___uniform, ___texture, ___unit ) \
		(___texture)->bind( ___unit );						  \
		___prg.Uniform1i( (char*)(___uniform), ___unit - GL_TEXTURE0 );

class GLSLProgram {
private:
    GLuint _programObject;
    GLuint _vertexShader;
    GLuint _geometryShader;
    GLuint _fragmentShader;
    GLuint _computeShader;

    GLchar* _vertexShaderSource;
    GLchar* _geometryShaderSource;
    GLchar* _fragmentShaderSource;
    GLchar* _computeShaderSource;

    bool computeShaderOK, vertexShaderOK, geometryShaderOK, fragmentShaderOK, linked;

    struct UniformVariable {
        unsigned int data;
        unsigned int type;
        char GLSLname[256];
        char TBname[256];
    };

    UniformVariable tbVariableDefault[16384];
    unsigned int nTweakBarVariablesDefault = 0;

    char _filename[16384];

    void unscrambleSource(GLchar* shaderSrc, int len) {
        // here you could unscramble obfuscated shaders
    }

    bool handleOneInclude(const GLchar* includePath, GLchar** shader, bool unscramble = false) {
        #ifdef _WIN32
        #define FLAGS
        #else
        #define FLAGS , std::regex::ECMAScript|std::regex::multiline
        #endif
        static std::regex includeRegex(R"(^#include\s*\"([^\"]+)\")" FLAGS);
        #undef FLAGS
        std::string shaderSrc(*shader);

        std::string includePathStr(includePath);
        std::filesystem::path currentFilePath(includePathStr);

        auto it = std::sregex_iterator(shaderSrc.begin(), shaderSrc.end(), includeRegex);
        if (it == std::sregex_iterator()) {
            return false;
        }

        static auto loadFileContent = [&](const std::string& filePath) {
            const std::ifstream fileStream(filePath);
            if (!fileStream.is_open()) {
                printf("[GLSL]: %c> '%s' not found, trying GLF's '%s'.\n", 192, filePath.c_str(), includePath);
                throw std::runtime_error("Failed to open file " + filePath);
            }
            std::stringstream buffer;
            buffer << fileStream.rdbuf();
            return buffer.str();
        };

        std::string includeDirective = it->str();
        std::string includeFile = (*it)[1].str();
        std::filesystem::path filePath = currentFilePath / includeFile;
        std::string includedContent = loadFileContent(filePath.string());

        std::string complete_shader = shaderSrc.replace(
            shaderSrc.find(includeDirective),
            includeDirective.length(),
            includedContent
        );

        auto* temp = new GLchar[complete_shader.size() + 1];
        memset(temp, 0, complete_shader.size() + 1);
        memcpy(temp, complete_shader.c_str(), complete_shader.size());

        delete *shader;
        *shader = temp;

        return true;
    }

    void handleIncludes(const GLchar* path, GLchar** shader, bool unscramble = false) {
        bool modified = true;

        while (modified) {
            modified = handleOneInclude(path, shader, unscramble);
        }
    }

    GLchar* loadSource(const char* filename, bool unscramble = false) {
        FILE* f = fopen(filename, "rb");
        if (f == NULL) {
            printf("[GLSL]: could not open %s.\n", filename);
            exit(1);
        }
        fseek(f, 0, SEEK_END);
        int len = ftell(f);
        fseek(f, 0, SEEK_SET);
        GLchar* shaderSrc = new GLchar[len + 1];
        fread(shaderSrc, 1, len, f);
        shaderSrc[len] = 0;

        strcpy(_filename, filename);

        if (unscramble)
            unscrambleSource(shaderSrc, len);

        fclose(f);

        char path[1024];
        strcpy(path, filename);
        for (int i = (int) strlen(path) - 1; i >= 0; i--)
            if (path[i] == '\\' || path[i] == '/') {
                path[i + 1] = 0;
                break;
            }

        handleIncludes(path, &shaderSrc, unscramble);

        return shaderSrc;
    }

    bool compileShader(GLuint& shader, GLchar* shaderSrc, const char* defineString = NULL) {
        if (defineString != NULL) {
            GLchar* s1 = shaderSrc;
            GLchar* s2 = strstr(shaderSrc, "#version");
            while (*s2 != 0 && *s2 != '\n')
                s2++;
            s2++;

            const char* s[3] = {s1, defineString, s2};
            GLuint len[3] = {(GLuint) (s2 - s1), (GLuint) strlen(defineString), (GLuint) strlen(s2)};
            glShaderSource(shader, 3, s, (GLint *) len);
        } else
            glShaderSource(shader, 1, (const GLchar **) &shaderSrc, NULL);

        GLchar source[10000];
        GLsizei length;
        glGetShaderSource(shader,10000,&length, source);
        glCompileShader(shader);

        GLint compileStatus;
        glGetObjectParameterivARB(shader, GL_OBJECT_COMPILE_STATUS_ARB, &compileStatus);
        if (!compileStatus) {
            fprintf(
                stderr, "[GLSL]: %c> compile problems (shader, possibly with includes, written to shader_error.glsl)\n",
                192);
            GLsizei slen;
            char errMsg[2048];
            glGetInfoLogARB(shader, 2047, &slen, errMsg);
            fprintf(stderr, "--------------------\n%s\n--------------------\n", errMsg);

            FILE* f = fopen("shader_error.glsl", "wt");
            fwrite(shaderSrc, 1, strlen(shaderSrc), f);
            fclose(f);

            return false;
        }

        glAttachShader(_programObject, shader);
        CheckErrorsGL();

        return true;
    }

    bool loadShader(GLuint& _shader, const char* filename, bool& shaderOK, GLchar** shaderSource,
                    bool unscramble = false, const char* defineString = NULL) {
        shaderOK = false;

        strcpy(_filename, filename);

        fprintf(stderr, "[GLSL]: reading '%s'\n", filename);

        char* shaderSrc = loadSource(filename, unscramble);

        if (!shaderSrc) {
            fprintf(stderr, "[GLSL]: error reading source file '%s'\n", filename);
            return false;
        }

        GLsizei nAttached;
        GLuint shaders[16];
        glGetAttachedShaders(_programObject, 16, &nAttached, shaders);
        for (int i = 0; i < nAttached; i++)
            if (shaders[i] == _shader) {
                glDetachShader(_programObject, _shader);
                break;
            }

        if (compileShader(_shader, shaderSrc, defineString)) {
            fprintf(stderr, "[GLSL]: %c> compile OK\n", 192);
            shaderOK = true;
        } else if (*shaderSource) {
            if (compileShader(_shader, *shaderSource, defineString)) {
                fprintf(stderr, "[GLSL]: %c> compile error, keeping old shader!\n", 192);
                shaderOK = true;
            }
        }

        if (shaderOK) {
            if (*shaderSource)
                delete[] *shaderSource;
            *shaderSource = shaderSrc;
        }

        return shaderOK;
    }

public:
    GLSLProgram() : computeShaderOK(false), vertexShaderOK(false), geometryShaderOK(false), fragmentShaderOK(false),
                    linked(false),
                    _computeShaderSource(NULL), _vertexShaderSource(NULL), _geometryShaderSource(NULL),
                    _fragmentShaderSource(NULL) {
        _programObject = glCreateProgram();
        _vertexShader = glCreateShader(GL_VERTEX_SHADER);
        _fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        _computeShader = glCreateShader(GL_COMPUTE_SHADER);
        _geometryShader = glCreateShader(GL_GEOMETRY_SHADER);
    }

    ~GLSLProgram() {
        if (vertexShaderOK)
            glDetachShader(_programObject, _vertexShader);
        glDeleteShader(_vertexShader);

        if (fragmentShaderOK)
            glDetachShader(_programObject, _fragmentShader);
        glDeleteShader(_fragmentShader);

        if (geometryShaderOK)
            glDetachShader(_programObject, _geometryShader);
        glDeleteShader(_geometryShader);

        if (computeShaderOK)
            glDetachShader(_programObject, _computeShader);
        glDeleteShader(_computeShader);

        glDeleteProgram(_programObject);
    }

    GLuint getProgramObject() { return _programObject; }
    GLuint getVertexShader() { return _vertexShader; }
    GLuint getGeometryShader() { return _geometryShader; }
    GLuint getFragmentShader() { return _fragmentShader; }
    GLuint getComputeShader() { return _computeShader; }

    GLchar* getVertexShaderSrc() { return _vertexShaderSource; }
    GLchar* getGeometryShaderSrc() { return _geometryShaderSource; }
    GLchar* getFragmentShaderSrc() { return _fragmentShaderSource; }
    GLchar* getComputeShaderSrc() { return _computeShaderSource; }

    bool loadComputeShader(const char* filename, const char* defineString) {
        return loadShader(_computeShader, filename, computeShaderOK, &_computeShaderSource, false, defineString);
    }

    bool loadComputeShader(const char* filename, bool unscramble = false, const char* defineString = NULL) {
        return loadShader(_computeShader, filename, computeShaderOK, &_computeShaderSource, unscramble, defineString);
    }

    bool loadVertexShader(const char* filename, bool unscramble = false, const char* defineString = NULL) {
        return loadShader(_vertexShader, filename, vertexShaderOK, &_vertexShaderSource, unscramble, defineString);
    }

    bool loadVertexShader(const char* filename, const char* defineString) {
        return loadShader(_vertexShader, filename, vertexShaderOK, &_vertexShaderSource, false, defineString);
    }

    bool loadGeometryShader(const char* filename, bool unscramble = false, GLint _GSInputType = -1,
                            GLint _GSOutputType = -1, GLint _GSOutputVertices = -1) {
        GLint GSInputType = (_GSInputType == -1) ? GL_TRIANGLES : _GSInputType;
        GLint GSOutputType = (_GSOutputType == -1) ? GL_TRIANGLE_STRIP : _GSOutputType;

        GLint GSMaxOutputVertices;
        glGetIntegerv(GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT, &GSMaxOutputVertices);
        GLint GSOutputVertices = (_GSOutputVertices == -1) ? GSMaxOutputVertices : _GSOutputVertices;

        if (GSOutputVertices > GSMaxOutputVertices)
            return false;

        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_INPUT_TYPE_EXT, GSInputType);
        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_OUTPUT_TYPE_EXT, GSOutputType);
        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_VERTICES_OUT_EXT, GSOutputVertices);

        return loadShader(_geometryShader, filename, geometryShaderOK, &_geometryShaderSource, unscramble);
    }

    bool loadGeometryShader(const char* filename, const char* defineString) {
        GLint GSInputType = GL_TRIANGLES;
        GLint GSOutputType = GL_TRIANGLE_STRIP;

        GLint GSMaxOutputVertices;
        glGetIntegerv(GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT, &GSMaxOutputVertices);
        GLint GSOutputVertices = GSMaxOutputVertices;

        if (GSOutputVertices > GSMaxOutputVertices)
            return false;

        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_INPUT_TYPE_EXT, GSInputType);
        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_OUTPUT_TYPE_EXT, GSOutputType);
        glProgramParameteriEXT(getProgramObject(), GL_GEOMETRY_VERTICES_OUT_EXT, GSOutputVertices);

        return loadShader(_geometryShader, filename, geometryShaderOK, &_geometryShaderSource, false, defineString);
    }

    bool loadFragmentShader(const char* filename, bool unscramble = false, const char* defineString = NULL) {
        return loadShader(_fragmentShader, filename, fragmentShaderOK, &_fragmentShaderSource, unscramble,
                          defineString);
    }

    bool loadFragmentShader(const char* filename, const char* defineString) {
        return loadShader(_fragmentShader, filename, fragmentShaderOK, &_fragmentShaderSource, false, defineString);
    }


    bool link() {
        bool is_compute_but_not_ok = _computeShaderSource != NULL && !computeShaderOK;
        bool is_renderpipeline_but_not_ok = _computeShaderSource == NULL && (!vertexShaderOK || !fragmentShaderOK);
        is_renderpipeline_but_not_ok = is_renderpipeline_but_not_ok || (_geometryShaderSource != NULL && !geometryShaderOK);
        if (is_compute_but_not_ok || is_renderpipeline_but_not_ok)
            return false;

        glLinkProgram(_programObject);

        GLchar buff[1024];
        GLsizei length;
        glGetProgramInfoLog(_programObject, 1024, &length, buff);
        if (length)
            printf("[GLSL]: %s\n", buff);

        GLint progLinkSuccess;
        glGetProgramiv(_programObject, GL_LINK_STATUS, &progLinkSuccess);

        if (!progLinkSuccess) {
            GLsizei slen;
            char errMsg[2048];
            glGetInfoLogARB(_programObject, 2047, &slen, errMsg);
            fprintf(stderr, "[GLSL]: shader link error:\n\n%s (related to %s)\n", errMsg, _filename);
            exit(1);
            return false;
        }
      
        return true;
    }

    bool bind() {
        if (!linked && !link())
            return false;

        linked = true;

        glUseProgram(_programObject);

        return true;
    }

    void setShaderUniformsDefault() {
        this->bind();
        for (unsigned int i = 0; i < nTweakBarVariablesDefault; i++) {
            switch (tbVariableDefault[i].type) {
                case SH_TYPE_BOOL32:
                    this->Uniform1i(tbVariableDefault[i].GLSLname, *(unsigned int *) &tbVariableDefault[i].data);
                    break;
                case SH_TYPE_INT32:
                    this->Uniform1i(tbVariableDefault[i].GLSLname, *(int *) &tbVariableDefault[i].data);
                    break;
                case SH_TYPE_UINT32:
                    this->Uniform1i(tbVariableDefault[i].GLSLname, *(unsigned int *) &tbVariableDefault[i].data);
                    break;
                case SH_TYPE_FLOAT:
                    this->Uniform1f(tbVariableDefault[i].GLSLname, *(float *) &tbVariableDefault[i].data);
                    break;
                default:
                    break;
            };
        }
    }

    void parseShaderSetDefault(const char* shaderSrc) {
        const char* src = shaderSrc;

    findNextVariable:
        src = strstr(src, "/*##");

        if (src == NULL) {
            setShaderUniformsDefault();
            nTweakBarVariablesDefault = 0;
            return;
        }

        const char* tok = src;
        while (tok != shaderSrc && !(tok[0] == '*' && tok[1] == '/')) {
            if (strstr(tok, "enum ") == tok) {
                const char* tokSafe = tok;

                // figure out variable name (find first comma or space before the first semicolor)
                tok = src;
                while (tok != shaderSrc && *tok != ';') tok--;
                const char* tok2 = tok;
                while (tok2 != shaderSrc && (*tok2 != ' ' && *tok2 != ',')) tok2--;
                tok2++;

                tok = tokSafe;

                tok += 5;
                while (*tok == ' ') tok++;
                // found enum -> special handling

                char title[512];
                sscanf(tok, "%s", title);
                tok += strlen(title);
                while (*tok == ' ') tok++;

                int nEnums;
                char buf[512];
                sscanf(tok, "%d", &nEnums);
                while (*tok != ' ') tok++;
                while (*tok == ' ') tok++;
                //sprintf( buf, "%d", nEnums );
                //tok += strlen( buf );

                for (int i = 0; i < nEnums; i++) {
                    sscanf(tok, "%s", buf);
                    tok += strlen(buf);
                    while (*tok == ' ') tok++;

                    char* buf2 = new char[strlen(buf) + 1];
                    strcpy(buf2, buf);
                }

                UniformVariable* var = &tbVariableDefault[nTweakBarVariablesDefault++];
                var->type = SH_TYPE_UINT32;
                memset(var->GLSLname, 0, 256);
                const char* tok3 = tok2;
                while (*tok3 != ' ' && *tok3 != ',' && *tok3 != ';') tok3++;
                strncpy(var->GLSLname, tok2, std::min(254, (int) (tok3 - tok2)));
                strcpy(var->TBname, title);
                var->data = 0;

                src = tok;
                goto findNextVariable;
            }
            tok++;
        }


        tok = src;

        // determine type of variable
        int type = -1;
        while (tok != shaderSrc && strstr(tok, "uniform ") != tok)
            tok--;

        tok += 8;

        if (strstr(tok, "unsigned int ") == tok) type = SH_TYPE_UINT32;
        if (strstr(tok, "int ") == tok) type = SH_TYPE_INT32;
        if (strstr(tok, "float ") == tok) type = SH_TYPE_FLOAT;
        if (strstr(tok, "bool ") == tok) type = SH_TYPE_BOOL32;

        if (type == -1)
            goto findNextVariable;

        // figure out variable name (find first comma or space before the first semicolor)
        tok = src;
        while (tok != shaderSrc && *tok != ';') tok--;
        const char* tok2 = tok;
        while (tok2 != shaderSrc && (*tok2 != ' ' && *tok2 != ',')) tok2--;
        tok2++;

        UniformVariable* var = &tbVariableDefault[nTweakBarVariablesDefault++];
        var->type = type;
        memset(var->GLSLname, 0, 256);
        strncpy(var->GLSLname, tok2, std::min(254, (int) (tok - tok2)));

        // skip "/*##"
        src += 4;

        float minV, maxV, step, defaultV;
        int iminV, imaxV, idefaultV;
        unsigned int uiminV, uimaxV, uidefaultV;
        switch (type) {
            case SH_TYPE_BOOL32:
                sscanf(src, "%s %d", var->TBname, &idefaultV);
                var->data = *(unsigned int *) &idefaultV;
                break;
            case SH_TYPE_INT32:
                sscanf(src, "%s %d %d %d", var->TBname, &idefaultV, &iminV, &imaxV);
                var->data = *(unsigned int *) &idefaultV;
                break;
            case SH_TYPE_UINT32:
                sscanf(src, "%s %d %d %d", var->TBname, &uidefaultV, &uiminV, &uimaxV);
                var->data = *(unsigned int *) &uidefaultV;
                break;
            case SH_TYPE_FLOAT:
                sscanf(src, "%s %f %f %f %f", var->TBname, &defaultV, &minV, &maxV, &step);
                var->data = *(unsigned int *) &defaultV;
                break;
            default:
                break;
        };

        goto findNextVariable;
    }


    void Uniform1f(const char* var, GLfloat v0) {
        glUniform1f(glGetUniformLocationARB(_programObject, var), v0);
    }

    void Uniform1ui(const char* var, GLuint v0) {
        glUniform1ui(glGetUniformLocationARB(_programObject, var), v0);
    }

    void Uniform1i(const char* var, GLint v0) {
        glUniform1i(glGetUniformLocationARB(_programObject, var), v0);
    }

    void Uniform2f(const char* var, GLfloat v0, GLfloat v1) {
        glUniform2f(glGetUniformLocationARB(_programObject, var), v0, v1);
    }

    void Uniform2i(const char* var, GLint v0, GLint v1) {
        glUniform2i(glGetUniformLocationARB(_programObject, var), v0, v1);
    }

    void Uniform3f(const char* var, GLfloat v0, GLfloat v1, GLfloat v2) {
        glUniform3f(glGetUniformLocationARB(_programObject, var), v0, v1, v2);
    }

    void Uniform3i(const char* var, GLint v0, GLint v1, GLint v2) {
        glUniform3i(glGetUniformLocationARB(_programObject, var), v0, v1, v2);
    }

    void Uniform4f(const char* var, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3) {
        glUniform4f(glGetUniformLocationARB(_programObject, var), v0, v1, v2, v3);
    }

    void Uniform4i(const char* var, GLint v0, GLint v1, GLint v2, GLint v3) {
        glUniform4i(glGetUniformLocationARB(_programObject, var), v0, v1, v2, v3);
    }

    void Uniform1fv(const char* var, GLsizei count, const GLfloat* v0) {
        glUniform1fv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform1iv(const char* var, GLsizei count, const GLint* v0) {
        glUniform1iv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform2fv(const char* var, GLsizei count, const GLfloat* v0) {
        glUniform2fv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform2iv(const char* var, GLsizei count, const GLint* v0) {
        glUniform2iv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform3fv(const char* var, GLsizei count, const GLfloat* v0) {
        glUniform3fv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform3iv(const char* var, GLsizei count, const GLint* v0) {
        glUniform3iv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform4fv(const char* var, GLsizei count, const GLfloat* v0) {
        glUniform4fv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void Uniform4iv(const char* var, GLsizei count, const GLint* v0) {
        glUniform4iv(glGetUniformLocationARB(_programObject, var), count, v0);
    }

    void UniformMatrix2fv(const char* var, GLsizei count, GLboolean transpose, const GLfloat* m) {
        glUniformMatrix2fvARB(glGetUniformLocationARB(_programObject, var), count, transpose, m);
    }

    void UniformMatrix3fv(const char* var, GLsizei count, GLboolean transpose, const GLfloat* m) {
        glUniformMatrix3fvARB(glGetUniformLocationARB(_programObject, var), count, transpose, m);
    }

    void UniformMatrix4fv(const char* var, GLsizei count, GLboolean transpose, const GLfloat* m) {
        glUniformMatrix4fvARB(glGetUniformLocationARB(_programObject, var), count, transpose, m);
    }
};

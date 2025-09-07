/*
    ________             _____      ________________________
    ___  __ \______________  /________  ____/__  /___  ____/
    __  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
    _  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
    /_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ code to parse GLSL shaders and automatically create AntTweakBar entries from them
*/

#include "stdafx.h"

#ifdef USE_TWEAK_BAR

TBVariable tbVariable[16384];
unsigned int nTweakBarVariables = 0;

void setShaderUniformsTweakBar() {
    GLSLProgram* last = NULL;
    for (unsigned int i = 0; i < nTweakBarVariables; i++) {
        if (last != tbVariable[i].GLSL_Program) {
            last = tbVariable[i].GLSL_Program;
            last->bind();
        }

        switch (tbVariable[i].type) {
            case TW_TYPE_BOOL32:
                tbVariable[i].GLSL_Program->Uniform1i(tbVariable[i].GLSLname, *(unsigned int *) &tbVariable[i].data);
                break;
            case TW_TYPE_INT32:
                tbVariable[i].GLSL_Program->Uniform1i(tbVariable[i].GLSLname, *(int *) &tbVariable[i].data);
                break;
            case TW_TYPE_UINT32:
                tbVariable[i].GLSL_Program->Uniform1i(tbVariable[i].GLSLname, *(unsigned int *) &tbVariable[i].data);
                break;
            case TW_TYPE_FLOAT:
                tbVariable[i].GLSL_Program->Uniform1f(tbVariable[i].GLSLname, *(float *) &tbVariable[i].data);
                break;
            default:
                break;
        };
    }
}

void parseShaderTweakBar(TwBar* bar, GLSLProgram* prg, const char* shaderSrc, const char* groupName) {
    const char* src = shaderSrc;

findNextVariable:
    src = strstr(src, "/*##");

    if (src == NULL)
        return;

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

            TwEnumVal* en = new TwEnumVal[nEnums];
            for (int i = 0; i < nEnums; i++) {
                en[i].Value = i;
                sscanf(tok, "%s", buf);
                tok += strlen(buf);
                while (*tok == ' ') tok++;

                char* buf2 = new char[strlen(buf) + 1];
                strcpy(buf2, buf);
                en[i].Label = buf2;
            }

            TBVariable* var = &tbVariable[nTweakBarVariables++];
            var->GLSL_Program = prg;
            var->type = TW_TYPE_UINT32;
            memset(var->GLSLname, 0, 256);
            const char* tok3 = tok2;
            while (*tok3 != ' ' && *tok3 != ',' && *tok3 != ';') tok3++;
            strncpy(var->GLSLname, tok2, std::min(254, (int) (tok3 - tok2)));
            strcpy(var->TBname, title);
            var->data = 0;

            sprintf(buf, "label='%s' group='%s'", var->TBname, groupName);
            TwType enumType = TwDefineEnum(title, en, nEnums);
            TwAddVarRW(bar, title, enumType, &var->data, buf);

            src = tok;
            goto findNextVariable;
        }
        tok++;
    }


    tok = src;

    // determine type of variable
    int type = -1;
    while (tok != shaderSrc && strstr(tok, "uniform ") != tok && strstr(tok, "uniform\t") != tok)
        tok--;

    tok += 8;

    if (strstr(tok, "unsigned int ") == tok) type = TW_TYPE_UINT32;
    if (strstr(tok, "int ") == tok) type = TW_TYPE_INT32;
    if (strstr(tok, "float ") == tok) type = TW_TYPE_FLOAT;
    if (strstr(tok, "bool ") == tok) type = TW_TYPE_BOOL32;

    if (type == -1)
        goto findNextVariable;

    // figure out variable name (find first comma or space before the first semicolor)
    tok = src;
    while (tok != shaderSrc && *tok != ';') tok--;
    const char* tok2 = tok;
    while (tok2 != shaderSrc && (*tok2 != ' ' && *tok2 != ',')) tok2--;
    tok2++;

    TBVariable* var = &tbVariable[nTweakBarVariables++];
    var->GLSL_Program = prg;
    var->type = type;
    memset(var->GLSLname, 0, 256);
    strncpy(var->GLSLname, tok2, std::min(254, (int) (tok - tok2)));

    // skip "/*##"
    src += 4;

    float minV, maxV, step, defaultV;
    int iminV, imaxV, idefaultV;
    unsigned int uiminV, uimaxV, uidefaultV;
    char buf[1024];
    switch (type) {
        case TW_TYPE_BOOL32:
            sscanf(src, "%s %d", var->TBname, &idefaultV);
            var->data = *(unsigned int *) &idefaultV;
            sprintf(buf, "label='%s' group='%s'", var->TBname, groupName);
            TwAddVarRW(bar, var->TBname, TW_TYPE_BOOL32, &var->data, buf);
            break;
        case TW_TYPE_INT32:
            sscanf(src, "%s %d %d %d", var->TBname, &idefaultV, &iminV, &imaxV);
            var->data = *(unsigned int *) &idefaultV;
            sprintf(buf, "label='%s' group='%s' min=%d max = %d", var->TBname, groupName, iminV, imaxV);
            TwAddVarRW(bar, var->TBname, TW_TYPE_INT32, &var->data, buf);
            break;
        case TW_TYPE_UINT32:
            sscanf(src, "%s %d %d %d", var->TBname, &uidefaultV, &uiminV, &uimaxV);
            var->data = *(unsigned int *) &uidefaultV;
            sprintf(buf, "label='%s' group='%s' min=%d max = %d", var->TBname, groupName, uiminV, uimaxV);
            TwAddVarRW(bar, var->TBname, TW_TYPE_UINT32, &var->data, buf);
            break;
        case TW_TYPE_FLOAT:
            sscanf(src, "%s %f %f %f %f", var->TBname, &defaultV, &minV, &maxV, &step);
            var->data = *(unsigned int *) &defaultV;
            sprintf(buf, "label='%s' group='%s' min=%2.8f max = %2.8f step = %2.8f", var->TBname, groupName, minV, maxV,
                    step);
            TwAddVarRW(bar, var->TBname, TW_TYPE_FLOAT, &var->data, buf);
            break;
        default:
            break;
    };

    goto findNextVariable;
}

#endif

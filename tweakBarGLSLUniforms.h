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

#pragma once

#ifndef TWEAKBAR_GLSL_UNIFORMS_H
#define TWEAKBAR_GLSL_UNIFORMS_H

struct TBVariable
{
	unsigned int data;
	unsigned int type;
	char GLSLname[ 256 ];
	char TBname[ 256 ];
	GLSLProgram  *GLSL_Program;
};

extern TBVariable tbVariable[ 16384 ];
extern unsigned int nTweakBarVariables;

extern void setShaderUniformsTweakBar();
extern void parseShaderTweakBar( TwBar *bar, GLSLProgram *prg, const char *shaderSrc, const char *groupName );
extern void parseShaderSetDefault( GLSLProgram *prg, const char *shaderSrc );

#endif



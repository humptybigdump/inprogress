/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ simple class to load/access environment maps
*/

#ifndef __ENVMAP_H
#define __ENVMAP_H

class EnvMap
{
private:
	GLSLProgram			prgSkybox;

	int					widthPC[64], heightPC[64];
	float				roughnessPC[64];

	float				*pEnvMap;
	int					widthEnvMap, heightEnvMap;

	Scene				*skybox;

	TextureManager		*texMan;

	glm::vec3 getRandomDirection();
	glm::vec2 direction2latlong( glm::vec3 dir );
	void getUV( glm::vec3 dir, int widthEnvMap, int heightEnvMap, int *s, int *t );

public:
	OGLTexture			*tEnvMap;
	OGLTexture			*tDiffMap;

	EnvMap() : tEnvMap(NULL), tDiffMap(NULL), pEnvMap(NULL), widthEnvMap(0), heightEnvMap(0), skybox(NULL)
	{
	}

	~EnvMap() 
	{
		if ( skybox)   delete skybox;
		if ( pEnvMap ) delete pEnvMap;
		if ( tEnvMap ) delete tEnvMap;
	};

	void initialize( TextureManager *_texMan, const char *envSpecFilename, const char *envDiffFilename = NULL )
	{
		texMan = _texMan;

		texMan->CreateTextureFromHDR( &tEnvMap, envSpecFilename );
		tEnvMap->bind();
		glGenerateMipmap( GL_TEXTURE_2D );
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR );

		tEnvMap->bind();

		glGetTexLevelParameteriv( GL_TEXTURE_2D, 0, GL_TEXTURE_WIDTH, &widthEnvMap ); 
		glGetTexLevelParameteriv( GL_TEXTURE_2D, 0, GL_TEXTURE_HEIGHT, &heightEnvMap ); 

		pEnvMap = new float[ 4 * widthEnvMap * heightEnvMap ];

		glGetTexImage( GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT, pEnvMap );

		if ( envDiffFilename )
		{
			texMan->CreateTextureFromHDR( &tDiffMap, envDiffFilename );
			tDiffMap->bind();
			glGenerateMipmap( GL_TEXTURE_2D );
			glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
			glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR );
		}


		prgSkybox.loadVertexShader  ( (char*)"./glf/shader/skybox.vp.glsl" );
		prgSkybox.loadFragmentShader( (char*)"./glf/shader/skybox.fp.glsl" );
        prgSkybox.link();

		skybox = new Scene( texMan );
		const char *attribsSkybox[1] = { "in_position" };
		mat4x4 matrix = glm::scale( glm::mat4( 1.0f), glm::vec3( 1.0f, 1.0f, 1.0f ) * 199.0f );
		skybox->loadOBJ( 0, prgSkybox.getProgramObject(), 1, (const char**)attribsSkybox, "sphere.obj", "./data/", true, &matrix );
	}

	void renderSkybox( glm::mat4 &matMVP, glm::mat4 &matLight, glm::vec3 &cp )
	{
		glDisable( GL_CULL_FACE );
		prgSkybox.bind();
		tEnvMap->bind( GL_TEXTURE0 );
		prgSkybox.UniformMatrix4fv( (char*)"matMVP", 1, false, glm::value_ptr( matMVP ) );
		prgSkybox.UniformMatrix4fv( (char*)"matLight", 1, false, &matLight[0][0] );
		prgSkybox.Uniform3fv( (char*)"camPos", 1, glm::value_ptr( cp ) );
		skybox->draw( &prgSkybox, 0 );
	}

	void bind(GLSLProgram* prg) {
		tEnvMap->bind(GL_TEXTURE5_ARB);
		prg->Uniform1i((char *) "tEnvMap", 5);
	}

	glm::vec3 getColor( const glm::vec3 &dir );
	glm::vec3 getMaxBrightness();
	void getUV( const glm::vec3 &dir, int *s, int *t );
};

#endif

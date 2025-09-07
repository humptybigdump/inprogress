/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ some helper routines for rendering widgets
*/

class Shapes
{
protected:
	GLSLProgram			prgRender, *userPrgRender;
	Scene				*scene;
	bool				userGLSLProgramProvided;

	mat4x4			matM_global, matVP;
	vec3			camPos, lightPos;

	
public:
	Shapes( TextureManager *texMan, GLSLProgram *userGLSLProgram = NULL ) 
	{
		userGLSLProgramProvided = false;

		if ( userGLSLProgram == NULL )
		{
			if ( !prgRender.loadVertexShader  ( (char*)"./shader/shapes.vp.glsl" ) ||
				 !prgRender.loadFragmentShader( (char*)"./shader/shapes.fp.glsl" ) )
			{
				exit( 1 );
			}
			prgRender.link();
			glBindFragDataLocation( prgRender.getProgramObject(), 0, "out_color" );

			scene = new Scene( texMan );
			const char *attribs[3] = { "in_position", "in_normal" };

			scene->loadOBJ( SCENE_SMOOTH, prgRender.getProgramObject(), 2, (const char**)attribs, "cylinder.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, prgRender.getProgramObject(), 2, (const char**)attribs, "cone.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, prgRender.getProgramObject(), 2, (const char**)attribs, "sphere.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, prgRender.getProgramObject(), 2, (const char**)attribs, "cube.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, prgRender.getProgramObject(), 2, (const char**)attribs, "pyramid.obj", "./data/shapes/", true );

			userPrgRender = &prgRender;
			userGLSLProgramProvided = true;
		} else
		{
			userPrgRender = userGLSLProgram;
			userGLSLProgramProvided = true;

			scene = new Scene( texMan );
			const char *attribs[3] = { "in_position", "in_normal" };

			scene->loadOBJ( SCENE_SMOOTH, userGLSLProgram->getProgramObject(), 2, (const char**)attribs, "cylinder.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, userGLSLProgram->getProgramObject(), 2, (const char**)attribs, "cone.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, userGLSLProgram->getProgramObject(), 2, (const char**)attribs, "sphere.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, userGLSLProgram->getProgramObject(), 2, (const char**)attribs, "cube.obj", "./data/shapes/", true );
			scene->loadOBJ( SCENE_SMOOTH, userGLSLProgram->getProgramObject(), 2, (const char**)attribs, "pyramid.obj", "./data/shapes/", true );
		}
	};
	~Shapes() {};

	void	beginDraw( const mat4 &_matM, const mat4 &_matVP, const vec3 &_camPos, const vec3 &_lightPos )
	{
		matVP = _matVP;
		matM_global = _matM;
		camPos = _camPos;
		lightPos = _lightPos;

		if ( userGLSLProgramProvided )
		{
			userPrgRender->bind();

			userPrgRender->Uniform3fv( (char*)"lightPos", 1, value_ptr( lightPos ) );
			userPrgRender->Uniform3fv( (char*)"camPos", 1, value_ptr( camPos ) );
			return;
		}

		prgRender.bind();

		prgRender.UniformMatrix4fv( (char*)"matM", 1, false, value_ptr( matM_global ) );
		mat4 matMVP = matVP * matM_global;
		prgRender.UniformMatrix4fv( (char*)"matMVP", 1, false, value_ptr( matMVP ) );

		prgRender.Uniform3fv( (char*)"lightPos", 1, value_ptr( lightPos ) );
		prgRender.Uniform3fv( (char*)"camPos", 1, value_ptr( camPos ) );
	}

	void	drawArrow( const vec3 &from_, const vec3 &to_, float thickness, const vec3 &color )
	{
		float spec[3] = { 1.0f, 1.0f, 1.0f };
		float emission[3] = { 0.0f, 0.0f, 0.0f };

		{
			userPrgRender->bind();
			userPrgRender->Uniform3fv( "objMatAmbient", 1, (GLfloat*)value_ptr( color ) );
			userPrgRender->Uniform3fv( "objMatDiffuse", 1, (GLfloat*)value_ptr( color ) );
			userPrgRender->Uniform3fv( "objMatSpecular", 1, spec );
			userPrgRender->Uniform3fv( "objMatEmission", 1, emission );
			userPrgRender->Uniform1f ( "objMatShininess", 4.0f );
		}

		vec3 to = to_, from = from_;
		vec3 z = to - from;
		float l = length( z );
		vec3 z_ = z / l;

		vec3 temp = vec3( 1.0f, 0.0f, 0.0f );
		if ( fabsf( dot( temp, z_ ) ) > 0.9f )
			temp = vec3( 0.0f, 1.0f, 0.0f );

		vec3 x, y;
		x = normalize( cross( z_, temp ) );
		y = normalize( cross( z_, x ) );

		mat3 matM3( -y, z_, x );

		mat4 translateFrom = translate( mat4( 1.0f ), from );
		mat4 matM( matM3 );

		mat4 matM_ = matM;

		matM = scale( matM, vec3( thickness, l - thickness, thickness ) );
		matM = translate( matM, vec3( 0.0f, 0.5f, 0.0f ) );

		mat4 matMVP = matVP * translateFrom * matM;

		mat4 matNrml = transpose( inverse( matM ) );

		userPrgRender->UniformMatrix4fv( (char*)"matNrml", 1, false, value_ptr( matNrml ) );
		userPrgRender->UniformMatrix4fv( (char*)"matMVP", 1, false, value_ptr( matMVP ) );

		scene->drawShape( 0, userPrgRender, 0 );

			
		matM_ = translate( matM_, vec3( 0.0f, l, 0.0f ) );
		matM_ = scale( matM_, vec3( thickness * 1.7f, thickness, thickness * 1.7f ) );
		matM_ = translate( matM_, vec3( 0.0f, -0.5f, 0.0f ) );

		matMVP = matVP * translateFrom * matM_;

		matNrml = transpose( inverse( matM ) );

		userPrgRender->UniformMatrix4fv( (char*)"matNrml", 1, false, value_ptr( matNrml ) );
		userPrgRender->UniformMatrix4fv( (char*)"matMVP", 1, false, value_ptr( matMVP ) );

		scene->drawShape( 1, userPrgRender, 0 );
		
	}

	void	drawCylinder( const vec3 &from_, const vec3 &to_, float thickness, const vec3 &color )
	{
		if ( userGLSLProgramProvided )
		{
			userPrgRender->bind();
		} else
		{
			printf("not implemented.\n" );
			exit(1);
		}

		float spec[3] = { 1.0f, 1.0f, 1.0f };
		float emission[3] = { 0.0f, 0.0f, 0.0f };
		userPrgRender->Uniform3fv( "objMatAmbient", 1, (GLfloat*)value_ptr( color ) );
		userPrgRender->Uniform3fv( "objMatDiffuse", 1, (GLfloat*)value_ptr( color ) );
		userPrgRender->Uniform3fv( "objMatSpecular", 1, spec );
		userPrgRender->Uniform3fv( "objMatEmission", 1, emission );
		userPrgRender->Uniform1f ( "objMatShininess", 4.0f );

		vec3 to = to_, from = from_;
		vec3 z = to - from;
		if ( dot( z, vec3( 1.0 ) ) < 0.0f )
		{
			z = to; to = from; from = z;
			z = to - from;
		}
		float l = length( z );
		vec3 z_ = z / l;

		vec3 temp = vec3( z_.y, z_.z, -z_.x );

		vec3 x, y;
		x = normalize( cross( z_, temp ) );
		y = normalize( cross( z_, x ) );

		mat3 matM3( -y, z_, x );

		mat4 translateFrom = translate( mat4( 1.0f ), from );
		mat4 matM( matM3 );



		mat4 matM_ = matM;

		matM = scale( matM, vec3( thickness, l, thickness ) );
		matM = translate( matM, vec3( 0.0f, 0.5f, 0.0f ) );
		matM = translateFrom * matM;
		mat4 matMVP = matVP * matM;

		mat4 matNrml = transpose( inverse( matM ) );

		userPrgRender->UniformMatrix4fv( (char*)"matNrml", 1, false, value_ptr( matNrml ) );
		userPrgRender->UniformMatrix4fv( (char*)"matMVP", 1, false, value_ptr( matMVP ) );

		scene->drawShape( 0, userPrgRender, 0 );
	}

	void	drawSphere( const vec3 &p, float r, const vec3 &color )
	{
		float spec[3] = { 1.0f, 1.0f, 1.0f };
		float emission[3] = { 0.0f, 0.0f, 0.0f };
		userPrgRender->Uniform3fv( "objMatAmbient", 1, (GLfloat*)value_ptr( color ) );
		userPrgRender->Uniform3fv( "objMatDiffuse", 1, (GLfloat*)value_ptr( color ) );
		userPrgRender->Uniform3fv( "objMatSpecular", 1, spec );
		userPrgRender->Uniform3fv( "objMatEmission", 1, emission );
		userPrgRender->Uniform1f ( "objMatShininess", 4.0f );

		mat4 matM( 1.0f );
		matM = translate( matM, p );
		matM = scale( matM, vec3( r ) );
		matM = matM_global * matM;
		
		if ( userGLSLProgramProvided )
		{
			userPrgRender->bind();

			mat4 matMVP = matVP * matM;

			mat4 matNrml = transpose( inverse( matM ) );

			userPrgRender->UniformMatrix4fv( (char*)"matNrml", 1, false, value_ptr( matNrml ) );
			userPrgRender->UniformMatrix4fv( (char*)"matMVP", 1, false, value_ptr( matMVP ) );

			scene->drawShape( 2, userPrgRender, 0 );
		} else
		{
			printf("not implemented.\n" );
			exit(1);
		}

	}

};

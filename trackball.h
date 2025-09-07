/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ trackball...
*/

#ifndef __TRACKBALL__H
#define __TRACKBALL__H

using namespace glm;

class TrackBall
{
private:
	vec3	sphereCamPos,
			sphereCenter;
	float	sphereRadius;

	float	rotationAngle;
	vec3	rotationAxis;

	vec3	curSpherePos,
			newSpherePos;

	int		tbAction;
	vec2	tbStrafe2DStart;
	vec3	tbStrafe3DView;
	float	tmStrafe3DZ;
	vec3	tbCameraStrafe;

	vec3	virtualCamPos,
			virtualCamTarget,
			virtualCamUp;

	mat4x4	matRotation, 
				trackballMatrix;
	mat4x4 camStrafe;

	bool tbHasUpdated;

	bool	spherePoint( const vec3& center, float r, const vec3& pscreen, vec3& psphere );
	void	setSphere( const vec3 &_center, float _radius );
	vec3	screenToWorld( int x, int y );
	void	updateMatrices();

public:
	TrackBall();
	~TrackBall();

	void	mouseWheel( int deltaPos );
	void	mouseMotion( int x, int y );
	void	mouseClick ( int button, int state, int x, int y );
	bool	keyboard( int key, int action );
	void	reset();

	bool	hasUpdated()
	{
		bool r = tbHasUpdated;
		tbHasUpdated = false;
		return r;
	}

	vec3	getCameraPosition();
	vec3	getCameraTarget();
	vec3	getCameraRight();
	vec3	getCameraUp();
	vec3	getCameraView();

	void	setupOpenGLMatrix();

	mat4x4	getStrafeMatrix();
	mat4x4	getMatrix();
	mat4x4	getNormalMatrix();
};


#endif


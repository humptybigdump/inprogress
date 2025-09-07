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

#include "stdafx.h"

using namespace glm;

#define TRACKBALL_MODE

#define TB_BUTTON_ROTATION	GLFW_MOUSE_BUTTON_LEFT
#define TB_BUTTON_ZOOM		GLFW_MOUSE_BUTTON_RIGHT
#define TB_BUTTON_STRAFE	GLFW_MOUSE_BUTTON_MIDDLE

#define TB_ACTION_ROTATION	1
#define TB_ACTION_STRAFE	2
#define TB_ACTION_ZOOM		4

void TrackBall::reset()
{
	setSphere( vec3( 0.0f, 0.0f, 0.0f ), 1.0f );

	sphereCamPos   = vec3( 0.0f, 0.0f, -2.0f );

	curSpherePos   = 
	newSpherePos   = vec3( 0.0f, 0.0f, 0.0f );

	rotationAxis   = vec3( 0.0f, 1.0f, 0.0f );

	rotationAngle  = 0.0f;

	tbStrafe3DView = vec3( 0.0f );
	tmStrafe3DZ    = 0.0f;

	tbAction       = 0;

	matRotation = mat4x4( 1.0f );
	trackballMatrix = mat4x4( 1.0f );

	tbCameraStrafe = vec3( 0.0f, 0.0f, -2.0f );

	updateMatrices();
}

TrackBall::TrackBall()
{
	reset();
	updateMatrices();
}

TrackBall::~TrackBall()
{
}

vec3	TrackBall::getCameraPosition()
{
#ifdef TRACKBALL_MODE
	vec3 n = -vec3( trackballMatrix[0][0], trackballMatrix[1][0], trackballMatrix[2][0] );
	vec3 u = -vec3( trackballMatrix[0][1], trackballMatrix[1][1], trackballMatrix[2][1] );
	vec3 d = -vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] );
	return trackballMatrix[3][1] * u + trackballMatrix[3][2] * d + trackballMatrix[3][0] * n;
#else
	return tbCameraStrafe;
#endif
}

vec3	TrackBall::getCameraRight()
{
	return vec3( trackballMatrix[0][0], trackballMatrix[1][0], trackballMatrix[2][0] );
}

vec3	TrackBall::getCameraTarget()
{
#ifdef TRACKBALL_MODE
	vec3 n = -vec3( trackballMatrix[0][0], trackballMatrix[1][0], trackballMatrix[2][0] );
	vec3 u = -vec3( trackballMatrix[0][1], trackballMatrix[1][1], trackballMatrix[2][1] );
	vec3 d = -vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] );
	return trackballMatrix[3][1] * u + trackballMatrix[3][0] * n;
#else
	return vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] ) + tbCameraStrafe;
#endif
}

vec3	TrackBall::getCameraUp()
{
	return vec3( trackballMatrix[0][1], trackballMatrix[1][1], trackballMatrix[2][1] );
}

vec3	TrackBall::getCameraView()
{
	return vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] );
}


void	TrackBall::setupOpenGLMatrix()
{
	glMultMatrixf( &trackballMatrix[0][0] );
}

void	TrackBall::setSphere( const vec3 &_center, float _radius )
{
	sphereCenter = _center;
	sphereRadius = _radius;
}

mat4x4	TrackBall::getStrafeMatrix()
{
	return camStrafe;
};

mat4x4	TrackBall::getMatrix()
{
	return trackballMatrix;
};

mat4x4	TrackBall::getNormalMatrix()
{
	return matRotation;
};

void	TrackBall::updateMatrices()
{
	// virtual camera
#ifdef TRACKBALL_MODE
	mat4x4 m = matRotation;
	vec3 translateWS = vec3( m * vec4( tbStrafe3DView, 0.0f ) );
	virtualCamPos    = vec3( 0.0f, 0.0f, tmStrafe3DZ - 2.0f ) - translateWS;
	virtualCamTarget = -translateWS;
	virtualCamUp     = vec3( 0.0f, 1.0f, 0.0f );

	// modelview trackball matrix 
	trackballMatrix = lookAt( virtualCamPos, virtualCamTarget, virtualCamUp );
	trackballMatrix = trackballMatrix * matRotation;
#else
	trackballMatrix = matRotation;
#endif
}

vec3	TrackBall::screenToWorld( int x, int y )
{ 
	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	float	s = (float)std::max( w, h );
	return vec3( 1.0f - x / s, y / s, 1.5f ) * 8.0f - 4.0f;
}


bool	TrackBall::spherePoint( const vec3& center, float r, const vec3& pscreen, vec3& psphere )
{ 
	vec3 camPos = vec3( 0.0f, 0.0f, -2.0f );
    vec3 v = normalize( pscreen - camPos ); 
	vec3 d = camPos - center;
	
	float dv = dot( d, v );
	float D  = dv * dv - dot( d, d ) + r * r;
	
	if ( D < 0 ) return false;

    psphere = sphereCamPos - v * ( dv + sqrtf( D ) );

	return true;
}

void TrackBall::mouseClick( int button, int state, int x, int y )
{
	int _w, _h;
	glfwGetWindowSize( glfwWindow, &_w, &_h );
	float w = (float)_w, h = (float)_h;

	if ( button == TB_BUTTON_ROTATION )
	{
		if( state == GLFW_PRESS )
		{
			vec3 psphere; 
			if ( spherePoint( sphereCenter, sphereRadius, screenToWorld( x, _h - y - 1 ), psphere ) ) {
				curSpherePos = psphere;
				newSpherePos = psphere;
				tbAction |= TB_ACTION_ROTATION;
			}
		} 
		if ( state == GLFW_RELEASE ) 
		{ 
			curSpherePos = newSpherePos;
			tbAction &= ~TB_ACTION_ROTATION;
			tbAction = 0;
		}
	}

	if ( button == TB_BUTTON_STRAFE || button == TB_BUTTON_ZOOM )
	{
		if( state == GLFW_PRESS )
		{
			tbStrafe2DStart = vec2( x, y ) / vec2( w, h );
			if ( button == TB_BUTTON_STRAFE )
				tbAction |= TB_ACTION_STRAFE; else
				tbAction |= TB_ACTION_ZOOM; 
		} 
		if ( state == GLFW_RELEASE ) 
		{ 
			curSpherePos = newSpherePos;
			if ( button == TB_BUTTON_STRAFE )
				tbAction &= ~TB_ACTION_STRAFE; else
				tbAction &= ~TB_ACTION_ZOOM; 
		}
	}

	tbHasUpdated = true;
}

void TrackBall::mouseWheel( int deltaPos )
{
	vec3 n =  vec3( trackballMatrix[0][0], trackballMatrix[1][0], trackballMatrix[2][0] );
	vec3 u =  vec3( trackballMatrix[0][1], trackballMatrix[1][1], trackballMatrix[2][1] );
	vec3 d = -vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] );
	vec3 p = trackballMatrix[3][1] * u + trackballMatrix[3][2] * d + trackballMatrix[3][0] * n;

	if ( deltaPos > 0 )
		tmStrafe3DZ += 0.125f * length( p ); else
		tmStrafe3DZ -= 0.125f * length( p );

	tmStrafe3DZ  = std::min( 3.0f, tmStrafe3DZ );

	updateMatrices();

	tbHasUpdated = true;
}

#define CLAMP(x, low, high)  (((x) > (high)) ? (high) : (((x) < (low)) ? (low) : (x)))

void TrackBall::mouseMotion( int x, int y )
{ 
	int _w, _h;
	glfwGetWindowSize( glfwWindow, &_w, &_h );
	float w = (float)_w, h = (float)_h;

	if ( tbAction & TB_ACTION_STRAFE || tbAction & TB_ACTION_ZOOM )
	{
		vec3 n =  vec3( trackballMatrix[0][0], trackballMatrix[1][0], trackballMatrix[2][0] );
		vec3 u =  vec3( trackballMatrix[0][1], trackballMatrix[1][1], trackballMatrix[2][1] );
		vec3 d = -vec3( trackballMatrix[0][2], trackballMatrix[1][2], trackballMatrix[2][2] );
		vec3 p = trackballMatrix[3][1] * u + trackballMatrix[3][2] * d + trackballMatrix[3][0] * n;

		vec2 tmDelta  = vec2( x, y ) / vec2( w, h ) - tbStrafe2DStart;
		tbStrafe2DStart = vec2( x, y ) / vec2( w, h );

		if ( tbAction & TB_ACTION_STRAFE )
		{
			tbStrafe3DView += n * tmDelta.x * length( p );
			tbStrafe3DView -= u * tmDelta.y * length( p );
		} else
		{
			tmStrafe3DZ -= tmDelta.y * length( p );
			tmStrafe3DZ  = std::min( 3.0f, tmStrafe3DZ );
		}

		tbHasUpdated = true;
	}

	if ( tbAction & TB_ACTION_ROTATION )
	{
		vec3 psphere;
		mat4x4 matrix;
		if ( spherePoint( sphereCenter, sphereRadius, screenToWorld( x, _h - y - 1 ), psphere ) ) 
		{
			if ( length( curSpherePos - psphere ) > 1e-4f )
			{
				rotationAxis = normalize( cross(curSpherePos-sphereCenter, psphere-sphereCenter) );

				vec3 t1 = curSpherePos-sphereCenter;
				vec3 t2 = psphere-sphereCenter;
				rotationAngle = -acosf( CLAMP(dot( t1, t2 ) / sphereRadius / sphereRadius, -1.0f, +1.0f) ) * -4.0f;

				rotationAxis = normalize(rotationAxis) * sinf(rotationAngle / 2.0f);
				float scalar = cosf(rotationAngle / 2.0f);
    
				fquat rotQuad( scalar, rotationAxis );
				matrix = toMat4(rotQuad);

				matRotation = matrix * matRotation;

				curSpherePos = psphere;
			}
		}
		tbHasUpdated = true;
	}

	updateMatrices();
}

bool	TrackBall::keyboard( int key, int action )
{
	#ifndef TRACKBALL_MODE
	float delta = 0.05f;

	mat4x4 m = ( trackballMatrix );
	vec3 u = -vec3( m[0][0], m[1][0], m[2][0] );
	vec3 n = -vec3( m[0][1], m[1][1], m[2][1] );
	vec3 d = -vec3( m[0][2], m[1][2], m[2][2] );

	switch ( key )
	{
	case 'W':
		tbCameraStrafe -= d * delta;
		tbHasUpdated = true;
		break;
	case 'S':
		tbCameraStrafe += d * delta;
		tbHasUpdated = true;
		break;
	case 'A':
		tbCameraStrafe -= u * delta;
		tbHasUpdated = true;
		break;
	case 'D':
		tbCameraStrafe += u * delta;
		tbHasUpdated = true;
		break;
	case 'Q':
		tbCameraStrafe += n * delta;
		tbHasUpdated = true;
		break;
	case 'E':
		tbCameraStrafe -= n * delta;
		tbHasUpdated = true;
		break;
	};

	if ( tbHasUpdated )
	{
		updateMatrices();
		return true;
	}

	#endif
	return false;
}

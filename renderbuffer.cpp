/*
  Copyright (c) 2005, 
	  Aaron Lefohn	(lefohn@cs.ucdavis.edu)
	  Adam Moerschell (atmoerschell@ucdavis.edu)
  All rights reserved.

  This software is licensed under the BSD open-source license. See
  http://www.opensource.org/licenses/bsd-license.php for more detail.

  *************************************************************
  Redistribution and use in source and binary forms, with or 
  without modification, are permitted provided that the following 
  conditions are met:

  Redistributions of source code must retain the above copyright notice, 
  this list of conditions and the following disclaimer. 

  Redistributions in binary form must reproduce the above copyright notice, 
  this list of conditions and the following disclaimer in the documentation 
  and/or other materials provided with the distribution. 

  Neither the name of the University of Californa, Davis nor the names of 
  the contributors may be used to endorse or promote products derived 
  from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
  THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF 
  THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
  OF SUCH DAMAGE.
*/
#include "stdafx.h"

#if defined(__ANDROID_API__)
#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO,LOG_TAG,__VA_ARGS__)
#define  LOGE(...)  __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,__VA_ARGS__)
#endif

using namespace std;

Renderbuffer::Renderbuffer()
  : m_bufId(_CreateBufferId())
{}

Renderbuffer::Renderbuffer(GLenum internalFormat, int width, int height, int nSamples)
  : m_bufId(_CreateBufferId())
{
  Set(internalFormat, width, height, nSamples);
}

Renderbuffer::~Renderbuffer()
{
  glDeleteRenderbuffers(1, &m_bufId);
}

void Renderbuffer::Bind() 
{
  glBindRenderbuffer(GL_RENDERBUFFER, m_bufId);
}

void Renderbuffer::Unbind() 
{
  glBindRenderbuffer(GL_RENDERBUFFER, 0);
}

void Renderbuffer::Set(GLenum internalFormat, int width, int height, int nSamples)
{
  int maxSize = Renderbuffer::GetMaxSize();
  if (width > maxSize || height > maxSize ) {
#if defined(__ANDROID_API__)
LOGI("Renderbuffer::Renderbuffer() ERROR: size too big (%d,%d)", width, height);
#else
    cerr << "Renderbuffer::Renderbuffer() ERROR:\n\t"
         << "Size too big (" << width << ", " << height << ")\n";
#endif
    return;
  }

  // Guarded bind
  GLint savedId = 0;
  glGetIntegerv( GL_RENDERBUFFER_BINDING, &savedId );
  if (savedId != (GLint)m_bufId) {
    Bind();
  }

  // Allocate memory for renderBuffer
  if ( nSamples == -1 )
	glRenderbufferStorage(GL_RENDERBUFFER, internalFormat, width, height ); else
	glRenderbufferStorageMultisample(GL_RENDERBUFFER, nSamples, internalFormat, width, height );

  // Guarded unbind
  if (savedId != (GLint)m_bufId) {
    glBindRenderbuffer(GL_RENDERBUFFER, savedId);
  }
}

GLuint Renderbuffer::GetId() const 
{
  return m_bufId;
}

GLint Renderbuffer::GetMaxSize()
{
  GLint maxAttach = 0;
  glGetIntegerv( GL_MAX_RENDERBUFFER_SIZE, &maxAttach );
  return maxAttach;
}

GLuint Renderbuffer::_CreateBufferId() 
{
  GLuint id = 0;
  glGenRenderbuffers(1, &id);
  return id;
}


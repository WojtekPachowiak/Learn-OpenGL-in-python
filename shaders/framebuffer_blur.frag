#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;

const float offset=1./300.;

void main()
{
    vec2 offsets[9]=vec2[](
        vec2(-offset,offset),// top-left
        vec2(0.f,offset),// top-center
        vec2(offset,offset),// top-right
        vec2(-offset,0.f),// center-left
        vec2(0.f,0.f),// center-center
        vec2(offset,0.f),// center-right
        vec2(-offset,-offset),// bottom-left
        vec2(0.f,-offset),// bottom-center
        vec2(offset,-offset)// bottom-right
    );
    
    float kernel[9]=float[](
        1./16,2./16,1./16,
        2./16,4./16,2./16,
        1./16,2./16,1./16
    );
    
    vec3 sampleTex[9];
    for(int i=0;i<9;i++)
    {
        sampleTex[i]=vec3(texture(screenTexture,TexCoords.st+offsets[i]));
    }
    vec3 col=vec3(0.);
    for(int i=0;i<9;i++)
    col+=sampleTex[i]*kernel[i];
    
    FragColor=vec4(col,1.);
}
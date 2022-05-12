# Deep Deformation (WIP !)
This is an early implementation of the "Fast and Deep Deformation Approximations".  The input data (meshes, bones, animation) are from Houdini extracted from **MocapBiped3** node. A neural network learns the non linear deformation from the smooth skinning and add details to the cheaper rigid skinning. 

### Remaining tasks

1. Convert offset in local space (currently world space)
2. Support multiple animation clips
3. Test with unseen animation clips
4. Analyse errors

### Simple Test

![DeepDeformation](https://github.com/vincentbonnetcg/DeepDeformation/blob/main/img/deepdeformation.gif)

### Body Test 

![CharacterDeformation](https://github.com/vincentbonnetcg/DeepDeformation/blob/main/img/characterdeformation.gif)



. Bailey, Stephen W., Dave Otte, Paul Dilorenzo, and James F. O'Brien. "Fast and deep deformation approximations." ACM Transactions on Graphics (TOG) 37, no. 4 (2018): 119.

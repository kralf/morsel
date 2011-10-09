#ifndef PERPSECTIVE_RANGE_CAMERA_H
#define PERPSECTIVE_RANGE_CAMERA_H

#include "morsel/sensors/range_camera.h"

class PerspectiveRangeCamera : public RangeCamera
{
public:
  PerspectiveRangeCamera(
    std::string name,
    double horizontalAngle,
    double verticalAngle,
    double horizontalFOV,
    double verticalFOV,
    int horizontalRays,
    int verticalRays,
    double minRange,
    double maxRange,
    int horizontalResolution = 128,
    int verticalResolution = 128,
    bool colorInfo = false
  );
  virtual ~PerspectiveRangeCamera();
protected:
  void setupLens();
  void setupRays();
};


#endif /*PERSPECTIVE_RANGE_CAMERA_H*/

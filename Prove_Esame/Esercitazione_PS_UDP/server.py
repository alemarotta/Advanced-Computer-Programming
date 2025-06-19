from skeleton import Skeleton
from skeletonImpl import SkeletonImpl

if __name__=="__main__":
    delegate=SkeletonImpl()
    skeleton=Skeleton("localhost",0,delegate)
    skeleton.run_Skeleton()
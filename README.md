# Path Planning in PyOCCT

<pre>


</pre>

## Description

<p> 
  DADI Lab에서 진행 중인 길찾기 알고리즘 관련 스터디 및 구현 결과를 관리하는 프로젝트입니다. 
</p>

<p>
  A project to manage the study and implementation results of the algorithm related to the wayfinding algorithm in progress at DADI Lab.
</p>

<pre>


</pre>

##  Envirment
<div>
  <p>● MS (OS)</p>
	<p>● PyOCCT (3D model Visualization)</p>
  <p>● Python (ProgramLanguage)</p>
</div>
<pre>


</pre>


##  Algorithms

<div>
  <p>● A* Algorithm in 3D</p>
  <p>● Theta* Algorithm in 3D</p>
  <p>● JPS Algorithm in 3D</p>
</div>

<pre>


</pre>


## Reference
<div>
  <p>Reference(A*)</p>
  <p>- https://www.youtube.com/watch?v=pUZhNMAqLbI</p>
	<pre>A* 알고리즘에 대한 기본적인 이론 및 알고리즘 구현 설명</pre>
  <p>- https://www.youtube.com/watch?v=gSpEep-c2mo</p>
	<pre>2D 그리드 맵 환경에서 A* 구현 설명</pre>
</div>

<div>
  <p>Reference(Theta*)</p>
  <p>- https://news.movel.ai/theta-star?x-host=news.movel.ai</p>
	<pre>Theta*와 A*관련 비교 분석에 관한 해외 기사</pre>
  <p>- https://github.com/GurkNathe/Pathfinding-Algorithms</p>
	<pre>Theta* 관련 오픈 소스(Python)</pre>
  <p>- http://idm-lab.org/bib/abstracts/papers/aaai07a.pdf</p>
	<pre>Theta* 소개 논문</pre>
</div>

<div>
  <p>Reference(Jps)</p>
  <p>- https://ojs.aaai.org/index.php/SOCS/article/view/21762</p>
	<pre>Jps 3D 소개 논문</pre>
  <p>- https://github.com/c2huc2hu/jps</p>
	<pre>Jps 관련 오픈 소스(Python)</pre>
</div>

## Sample of path planning example
![image](https://github.com/DADILabKIT/Path_Planning_in_OCCT/assets/128150322/e98708eb-e6a1-4fc8-92b0-19a6ad0603a2)
  <p>● A* Algorithm in 3D Grid Map</p>
  
![image](https://github.com/DADILabKIT/Path_Planning_in_OCCT/assets/128150322/02dd0f98-50e1-49ec-9baf-71d784bdc6b9)
  <p>● Theta* Algorithm in 3D Grid Map</p>
  
![image](https://github.com/DADILabKIT/Path_Planning_in_OCCT/assets/128150322/3a3d050a-dd9a-4138-894e-9d6a274996d7)
  <p>● JPS Algorithm in 3D Grid Map</p>
<pre>


</pre>

## How to Use

<div> 
  <pre>1. 먼저, 아나콘다 가상환경과 파이썬을 설치한다.</pre>
  <pre>2. 다음 PyOCCT 공식 깃허브 사이트의 가이드를 참고하여 가상환경에 PyOCCT를 설치한다. 
  (PyOCCT : https://github.com/trelau/pyOCCT)</pre>
  <pre>3. 설치한 후 Vscode에서 폴더를 연 후 visualTest를 실행 후에 Bool Map에서 6*6*6 맵들을 터미널에 입력한다.
  (0은 자유 공간, 1은 장애물)</pre>
</div>

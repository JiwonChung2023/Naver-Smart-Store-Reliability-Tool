# Naver-Smart-Store-Reliability-Tool(NSSRT)

## 네이버 스마트 스토어는 과연 안전할까? 거기서 소비자가 믿고 구매하는 이유가 뭘까?

### 프로젝트 아이디어 도출점

현재 2023년 기준 네이버 스마트 스토어는 한국인이 애용하는 쇼핑 사이트 중 하나입니다. 쇼핑하기 간편하고 네이버라는 플랫폼에 신뢰성이 있기 때문입니다. 하지만 최근 신문 기사에 의하면 스마트 스토어를 활용한 사기 수법이 수면으로 떠오르고 있습니다. 판매 제품 가격을 상대적으로 저렴히 올려 구매를 유도한 후 쇼핑 페이지를 폐쇄하는 등 그 수법도 다양하다고 하는데
그러면 소비자 피해를 막으려면 어떻게 해야 할까요? 저희 팀의 프로젝트 'Naver Smart Store Reliability Tool(NSSRT)'가 그에 대한 답입니다. NSSRT는 소비자 보호를 돕고자 스마트 스토어 입점 업체의 신뢰도를 계산하고 보여줍니다.

### 데이터 수집

수집기간 : 2023-04-05 ~ 04-15

수집방법 : 
Step1: 리뷰 조작 커뮤니티에 있는 스마트 스토어 사기 의심 업체 목록을 수집합니다.
Step2: 스마트 스토어 업체 홈페이지 들어가서 사기 의심 업체의 공통 특성을 분석합니다.
Step3: 특성 중 상대적으로 중요한 것에 가중치를 두고 모델을 생성합니다. 


### 데이터 분석 결과 예상
1. 판매 상품의 카테고리가 일관적이지 않고 전문적이지 않을시 사기 의심 업체일 것이다.
2. 판매자의 톡톡 응답률이 낮을시 사기 의심 업체일 것이다.
3. 판매자의 Q&A 응답률이 낮을시 사기 의심 업체일 것이다.
4. 판매자의 주소가 사무실이나 회사가 아닌 아파트나 일반 주택일시 사기 의심 업체일 것이다.
5. 리뷰가 현저히 적거나 아예 없을시 사기 의심 업체일 것이다.
6. 관심 고객수 or 스토어 찜 수가 리뷰의 수에 비해 현저히 적을시 사기 의심 업체일 것이다.
7. 판매자 정보에 사업자등록번호가 없을시 사기 의심 업체일 것이다.
8. 공정거래위원회에 사업자등록번호가 조회가 안될시 사기 의심 업체일 것이다.
9. 공정거래위원회에 사업자등록번호 조회시 신고 일자가 너무 최근일시 사기 의심 업체일 것이다.
10. 가격이 다른 경쟁 업체에 비해 낮을시 사기 의심 업체일 것이다.



### 참고 PPT 자료
[프로젝트 전개 과정 설명 PPT](./NSSRT.pptx)

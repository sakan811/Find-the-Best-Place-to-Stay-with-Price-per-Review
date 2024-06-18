import datetime
import os
import sys

import pandas as pd
import requests
from loguru import logger

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])
logger.add('find_best_place_to_stay.log', level='INFO',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def get_header() -> dict:
    """
    Return header.
    :return: Header as a dictionary.
    """
    logger.info("Getting header...")
    return {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Booking-Csrf-Token": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJjb250ZXh0LWVucmljaG1lbnQtYXBpIiwic3ViIjoiY3NyZi10b2tlbiIsImlhdCI6MTcxODYyNTQ2NywiZXhwIjoxNzE4NzExODY3fQ.CAooc42_J_78rrJe-e2kgLUyRvd_JBzuo2G8MP2V6veKwH5-TfikWdjTK2yBOfEe_Xl_IxDMFZOl-Q3qgvWp5A",
        "X-Booking-Context-Action-Name": "searchresults_irene",
        "X-Booking-Context-Aid": "304142",
        'X-Booking-Et-Serialized-State': 'EjwSq9PIMG0Wo3kB1frx34bv9-QpErp-BGeatPFobVv6jCzqqAw4Gg8OdLtw5fMdx',
        'X-Booking-Pageview-Id': 'cd7f472c35d2008c',
        'X-Booking-Site-Type-Id': '1',
        'X-Booking-Topic': 'capla_browser_b-search-web-searchresults',
        "Sec-Ch-Ua-Platform": "Windows",
        "Origin": "https://www.booking.com",
        "Priority": "u=1, i",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }


def get_graphql_query(
        city: str,
        check_in: str,
        check_out: str,
        group_adults: int,
        num_rooms: int,
        group_children: int,
        hotel_filter: bool,
        page_offset: int = 0) -> dict:
    """
    Return graphql query.
    :param city: City where the hotels are located.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param group_adults: Number of adults.
    :param num_rooms: Number of rooms.
    :param group_children: Number of children.
    :param hotel_filter: If True, scrape only hotel properties, else scrape all properties.
                        Default is False.
    :param page_offset: Page offset.
                        Default is 0.
    :return: Graphql query as a dictionary.
    """
    logger.debug("Getting graphql query...")
    if hotel_filter:
        selected_filter = {"selectedFilters": "ht_id=204"}
    else:
        selected_filter = {}

    return {
        "operationName": "FullSearch",
        "variables": {
            "input": {
                "acidCarouselContext": None,
                "childrenAges": [
                    0
                ],
                "dates": {
                    "checkin": check_in,
                    "checkout": check_out
                },
                "doAvailabilityCheck": False,
                "encodedAutocompleteMeta": None,
                "enableCampaigns": True,
                "filters": selected_filter,
                "flexibleDatesConfig": {
                    "broadDatesCalendar": {
                        "checkinMonths": [],
                        "los": [],
                        "startWeekdays": []
                    },
                    "dateFlexUseCase": "DATE_RANGE",
                    "dateRangeCalendar": {
                        "checkin": [
                            check_in
                        ],
                        "checkout": [
                            check_out
                        ]
                    }
                },
                "forcedBlocks": None,
                "location": {
                    "searchString": city,
                    "destType": "CITY"
                },
                "metaContext": {
                    "metaCampaignId": 0,
                    "externalTotalPrice": None,
                    "feedPrice": None,
                    "hotelCenterAccountId": None,
                    "rateRuleId": None,
                    "dragongateTraceId": None,
                    "pricingProductsTag": None
                },
                "nbRooms": num_rooms,
                "nbAdults": group_adults,
                "nbChildren": group_children,
                "needsRoomsMatch": False,
                "optionalFeatures": {
                    "forceArpExperiments": True,
                    "testProperties": False
                },
                "pagination": {
                    "rowsPerPage": 100,
                    "offset": page_offset
                },
                "rawQueryForSession": "/searchresults.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaN0BiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuAK-xsCzBsACAdICJGE1MjFhMmVkLTYyNDgtNDg0MC04NTcxLWM4NzcxYTFhZWQ2OdgCBeACAQ&sid=56b869f50c3ca1f92a94af874ce38d13&aid=304142&ss=Osaka&ssne=Osaka&ssne_untouched=Osaka&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-240905&dest_type=city&checkin=2024-07-05&checkout=2024-07-06&group_adults=1&no_rooms=1&group_children=1&age=0&selected_currency=USD",
                "referrerBlock": {
                    "blockName": "searchbox"
                },
                "sbCalendarOpen": False,
                "sorters": {
                    "selectedSorter": None,
                    "referenceGeoId": None,
                    "tripTypeIntentId": None
                },
                "travelPurpose": 2,
                "seoThemeIds": [],
                "useSearchParamsFromSession": True,
                "merchInput": {
                    "testCampaignIds": []
                }
            },
            "carouselLowCodeExp": False
        },
        "extensions": {},
        "query": "query FullSearch($input: SearchQueryInput!, $carouselLowCodeExp: Boolean!) {\n  searchQueries {\n    "
                 "search(input: $input) {\n      ...FullSearchFragment\n      __typename\n    }\n    __typename\n  "
                 "}\n}\n\nfragment FullSearchFragment on SearchQueryOutput {\n  banners {\n    ...Banner\n    __typename\n  "
                 "}\n  breadcrumbs {\n    ... on SearchResultsBreadcrumb {\n      ...SearchResultsBreadcrumb\n      "
                 "__typename\n    }\n    ... on LandingPageBreadcrumb {\n      ...LandingPageBreadcrumb\n      __typename\n "
                 "   }\n    __typename\n  }\n  carousels {\n    ...Carousel\n    __typename\n  }\n  destinationLocation {\n "
                 "   ...DestinationLocation\n    __typename\n  }\n  entireHomesSearchEnabled\n  dateFlexibilityOptions {\n  "
                 "  enabled\n    __typename\n  }\n  flexibleDatesConfig {\n    broadDatesCalendar {\n      checkinMonths\n  "
                 "    los\n      startWeekdays\n      losType\n      __typename\n    }\n    dateFlexUseCase\n    "
                 "dateRangeCalendar {\n      flexWindow\n      checkin\n      checkout\n      __typename\n    }\n    "
                 "__typename\n  }\n  filters {\n    ...FilterData\n    __typename\n  }\n  filtersTrackOnView {\n    type\n  "
                 "  experimentHash\n    value\n    __typename\n  }\n  appliedFilterOptions {\n    ...FilterOption\n    "
                 "__typename\n  }\n  recommendedFilterOptions {\n    ...FilterOption\n    __typename\n  }\n  pagination {\n "
                 "   nbResultsPerPage\n    nbResultsTotal\n    __typename\n  }\n  tripTypes {\n    ...TripTypesData\n    "
                 "__typename\n  }\n  results {\n    ...BasicPropertyData\n    ...MatchingUnitConfigurations\n    "
                 "...PropertyBlocks\n    ...BookerExperienceData\n    priceDisplayInfoIrene {\n      "
                 "...PriceDisplayInfoIrene\n      __typename\n    }\n    licenseDetails {\n      nextToHotelName\n      "
                 "__typename\n    }\n    isTpiExclusiveProperty\n    propertyCribsAvailabilityLabel\n    "
                 "mlBookingHomeTags\n    trackOnView {\n      experimentTag\n      __typename\n    }\n    __typename\n  }\n "
                 " searchMeta {\n    ...SearchMetadata\n    __typename\n  }\n  sorters {\n    option {\n      "
                 "...SorterFields\n      __typename\n    }\n    __typename\n  }\n  oneOfThreeDeal {\n    "
                 "...OneOfThreeDeal\n    __typename\n  }\n  zeroResultsSection {\n    ...ZeroResultsSection\n    "
                 "__typename\n  }\n  rocketmilesSearchUuid\n  previousSearches {\n    ...PreviousSearches\n    __typename\n "
                 " }\n  frontierThemes {\n    ...FrontierThemes\n    __typename\n  }\n  merchComponents {\n    "
                 "...MerchRegionIrene\n    __typename\n  }\n  wishlistData {\n    numProperties\n    __typename\n  }\n  "
                 "seoThemes {\n    id\n    caption\n    __typename\n  }\n  __typename\n}\n\nfragment BasicPropertyData on "
                 "SearchResultProperty {\n  acceptsWalletCredit\n  basicPropertyData {\n    accommodationTypeId\n    id\n   "
                 " isTestProperty\n    location {\n      address\n      city\n      countryCode\n      __typename\n    }\n  "
                 "  pageName\n    ufi\n    photos {\n      main {\n        highResUrl {\n          relativeUrl\n          "
                 "__typename\n        }\n        lowResUrl {\n          relativeUrl\n          __typename\n        }\n      "
                 "  highResJpegUrl {\n          relativeUrl\n          __typename\n        }\n        lowResJpegUrl {\n     "
                 "     relativeUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n "
                 "   reviewScore: reviews {\n      score: totalScore\n      reviewCount: reviewsCount\n      "
                 "totalScoreTextTag {\n        translation\n        __typename\n      }\n      showScore\n      "
                 "secondaryScore\n      secondaryTextTag {\n        translation\n        __typename\n      }\n      "
                 "showSecondaryScore\n      __typename\n    }\n    externalReviewScore: externalReviews {\n      score: "
                 "totalScore\n      reviewCount: reviewsCount\n      showScore\n      totalScoreTextTag {\n        "
                 "translation\n        __typename\n      }\n      __typename\n    }\n    starRating {\n      value\n      "
                 "symbol\n      caption {\n        translation\n        __typename\n      }\n      tocLink {\n        "
                 "translation\n        __typename\n      }\n      showAdditionalInfoIcon\n      __typename\n    }\n    "
                 "isClosed\n    paymentConfig {\n      installments {\n        minPriceFormatted\n        maxAcceptCount\n  "
                 "      __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  badges {\n    caption {\n      "
                 "translation\n      __typename\n    }\n    closedFacilities {\n      startDate\n      endDate\n      "
                 "__typename\n    }\n    __typename\n  }\n  customBadges {\n    showSkiToDoor\n    "
                 "showBhTravelCreditBadge\n    showOnlineCheckinBadge\n    __typename\n  }\n  description {\n    text\n    "
                 "__typename\n  }\n  displayName {\n    text\n    translationTag {\n      translation\n      __typename\n   "
                 " }\n    __typename\n  }\n  geniusInfo {\n    benefitsCommunication {\n      header {\n        title\n     "
                 "   __typename\n      }\n      items {\n        title\n        __typename\n      }\n      __typename\n    "
                 "}\n    geniusBenefits\n    geniusBenefitsData {\n      hotelCardHasFreeBreakfast\n      "
                 "hotelCardHasFreeRoomUpgrade\n      sortedBenefits\n      __typename\n    }\n    showGeniusRateBadge\n    "
                 "__typename\n  }\n  location {\n    displayLocation\n    mainDistance\n    "
                 "publicTransportDistanceDescription\n    skiLiftDistance\n    beachDistance\n    nearbyBeachNames\n    "
                 "beachWalkingTime\n    geoDistanceMeters\n    __typename\n  }\n  mealPlanIncluded {\n    mealPlanType\n    "
                 "text\n    __typename\n  }\n  persuasion {\n    autoextended\n    geniusRateAvailable\n    highlighted\n   "
                 " preferred\n    preferredPlus\n    showNativeAdLabel\n    nativeAdId\n    nativeAdsCpc\n    "
                 "nativeAdsTracking\n    sponsoredAdsData {\n      isDsaCompliant\n      legalEntityName\n      "
                 "sponsoredAdsDesign\n      __typename\n    }\n    __typename\n  }\n  policies {\n    "
                 "showFreeCancellation\n    showNoPrepayment\n    enableJapaneseUsersSpecialCase\n    __typename\n  }\n  "
                 "ribbon {\n    ribbonType\n    text\n    __typename\n  }\n  recommendedDate {\n    checkin\n    checkout\n "
                 "   lengthOfStay\n    __typename\n  }\n  showGeniusLoginMessage\n  hostTraderLabel\n  soldOutInfo {\n    "
                 "isSoldOut\n    messages {\n      text\n      __typename\n    }\n    alternativeDatesMessages {\n      "
                 "text\n      __typename\n    }\n    __typename\n  }\n  nbWishlists\n  visibilityBoosterEnabled\n  "
                 "showAdLabel\n  isNewlyOpened\n  propertySustainability {\n    isSustainable\n    tier {\n      type\n     "
                 " __typename\n    }\n    facilities {\n      id\n      __typename\n    }\n    certifications {\n      "
                 "name\n      __typename\n    }\n    chainProgrammes {\n      chainName\n      programmeName\n      "
                 "__typename\n    }\n    levelId\n    __typename\n  }\n  seoThemes {\n    caption\n    __typename\n  }\n  "
                 "relocationMode {\n    distanceToCityCenterKm\n    distanceToCityCenterMiles\n    "
                 "distanceToOriginalHotelKm\n    distanceToOriginalHotelMiles\n    phoneNumber\n    __typename\n  }\n  "
                 "bundleRatesAvailable\n  __typename\n}\n\nfragment Banner on Banner {\n  name\n  type\n  isDismissible\n  "
                 "showAfterDismissedDuration\n  position\n  requestAlternativeDates\n  merchId\n  title {\n    text\n    "
                 "__typename\n  }\n  imageUrl\n  paragraphs {\n    text\n    __typename\n  }\n  metadata {\n    key\n    "
                 "value\n    __typename\n  }\n  pendingReviewInfo {\n    propertyPhoto {\n      lowResUrl {\n        "
                 "relativeUrl\n        __typename\n      }\n      lowResJpegUrl {\n        relativeUrl\n        "
                 "__typename\n      }\n      __typename\n    }\n    propertyName\n    urlAccessCode\n    __typename\n  }\n  "
                 "nbDeals\n  primaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n   "
                 "   context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    "
                 "__typename\n  }\n  secondaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n     "
                 " name\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    "
                 "}\n    __typename\n  }\n  iconName\n  flexibleFilterOptions {\n    optionId\n    filterName\n    "
                 "__typename\n  }\n  trackOnView {\n    type\n    experimentHash\n    value\n    __typename\n  }\n  "
                 "dateFlexQueryOptions {\n    text {\n      text\n      __typename\n    }\n    action {\n      name\n      "
                 "context {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    "
                 "isApplied\n    __typename\n  }\n  __typename\n}\n\nfragment Carousel on Carousel {\n  "
                 "aggregatedCountsByFilterId\n  carouselId\n  position\n  contentType\n  hotelId\n  name\n  "
                 "soldoutProperties\n  priority\n  themeId\n  frontierThemeIds\n  title {\n    text\n    __typename\n  }\n  "
                 "slides {\n    captionText {\n      text\n      __typename\n    }\n    name\n    photoUrl\n    subtitle {"
                 "\n      text\n      __typename\n    }\n    type\n    title {\n      text\n      __typename\n    }\n    "
                 "action {\n      context {\n        key\n        value\n        __typename\n      }\n      __typename\n    "
                 "}\n    __typename\n  }\n  __typename\n}\n\nfragment DestinationLocation on DestinationLocation {\n  name "
                 "{\n    text\n    __typename\n  }\n  inName {\n    text\n    __typename\n  }\n  countryCode\n  ufi\n  "
                 "__typename\n}\n\nfragment FilterData on Filter {\n  trackOnView {\n    type\n    experimentHash\n    "
                 "value\n    __typename\n  }\n  trackOnClick {\n    type\n    experimentHash\n    value\n    __typename\n  "
                 "}\n  name\n  field\n  category\n  filterStyle\n  title {\n    text\n    translationTag {\n      "
                 "translation\n      __typename\n    }\n    __typename\n  }\n  subtitle\n  options {\n    parentId\n    "
                 "genericId\n    trackOnView {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    "
                 "trackOnClick {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnSelect "
                 "{\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelect {\n      "
                 "type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnViewPopular {\n      type\n  "
                 "    experimentHash\n      value\n      __typename\n    }\n    trackOnClickPopular {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    trackOnSelectPopular {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelectPopular {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    ...FilterOption\n    __typename\n  }\n  "
                 "filterLayout {\n    isCollapsable\n    collapsedCount\n    __typename\n  }\n  stepperOptions {\n    min\n "
                 "   max\n    default\n    selected\n    title {\n      text\n      translationTag {\n        translation\n "
                 "       __typename\n      }\n      __typename\n    }\n    field\n    labels {\n      text\n      "
                 "translationTag {\n        translation\n        __typename\n      }\n      __typename\n    }\n    "
                 "trackOnView {\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnClick {"
                 "\n      type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnSelect {\n      "
                 "type\n      experimentHash\n      value\n      __typename\n    }\n    trackOnDeSelect {\n      type\n     "
                 " experimentHash\n      value\n      __typename\n    }\n    trackOnClickDecrease {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    trackOnClickIncrease {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    trackOnDecrease {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    trackOnIncrease {\n      type\n      "
                 "experimentHash\n      value\n      __typename\n    }\n    __typename\n  }\n  sliderOptions {\n    min\n   "
                 " max\n    minSelected\n    maxSelected\n    minPriceStep\n    minSelectedFormatted\n    currency\n    "
                 "histogram\n    selectedRange {\n      translation\n      __typename\n    }\n    __typename\n  }\n  "
                 "__typename\n}\n\nfragment FilterOption on Option {\n  optionId: id\n  count\n  selected\n  urlId\n  "
                 "source\n  additionalLabel {\n    text\n    translationTag {\n      translation\n      __typename\n    }\n "
                 "   __typename\n  }\n  value {\n    text\n    translationTag {\n      translation\n      __typename\n    "
                 "}\n    __typename\n  }\n  starRating {\n    value\n    symbol\n    caption {\n      translation\n      "
                 "__typename\n    }\n    showAdditionalInfoIcon\n    __typename\n  }\n  __typename\n}\n\nfragment "
                 "LandingPageBreadcrumb on LandingPageBreadcrumb {\n  destType\n  name\n  urlParts\n  "
                 "__typename\n}\n\nfragment MatchingUnitConfigurations on SearchResultProperty {\n  "
                 "matchingUnitConfigurations {\n    commonConfiguration {\n      name\n      unitId\n      "
                 "bedConfigurations {\n        beds {\n          count\n          type\n          __typename\n        }\n   "
                 "     nbAllBeds\n        __typename\n      }\n      nbAllBeds\n      nbBathrooms\n      nbBedrooms\n      "
                 "nbKitchens\n      nbLivingrooms\n      nbUnits\n      unitTypeNames {\n        translation\n        "
                 "__typename\n      }\n      localizedArea {\n        localizedArea\n        unit\n        __typename\n     "
                 " }\n      __typename\n    }\n    unitConfigurations {\n      name\n      unitId\n      bedConfigurations "
                 "{\n        beds {\n          count\n          type\n          __typename\n        }\n        nbAllBeds\n  "
                 "      __typename\n      }\n      apartmentRooms {\n        config {\n          roomId: id\n          "
                 "roomType\n          bedTypeId\n          bedCount: count\n          __typename\n        }\n        "
                 "roomName: tag {\n          tag\n          translation\n          __typename\n        }\n        "
                 "__typename\n      }\n      nbAllBeds\n      nbBathrooms\n      nbBedrooms\n      nbKitchens\n      "
                 "nbLivingrooms\n      nbUnits\n      unitTypeNames {\n        translation\n        __typename\n      }\n   "
                 "   localizedArea {\n        localizedArea\n        unit\n        __typename\n      }\n      unitTypeId\n  "
                 "    __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PropertyBlocks on "
                 "SearchResultProperty {\n  blocks {\n    blockId {\n      roomId\n      occupancy\n      policyGroupId\n   "
                 "   packageId\n      mealPlanId\n      __typename\n    }\n    finalPrice {\n      amount\n      currency\n "
                 "     __typename\n    }\n    originalPrice {\n      amount\n      currency\n      __typename\n    }\n    "
                 "onlyXLeftMessage {\n      tag\n      variables {\n        key\n        value\n        __typename\n      "
                 "}\n      translation\n      __typename\n    }\n    freeCancellationUntil\n    hasCrib\n    blockMatchTags "
                 "{\n      childStaysForFree\n      __typename\n    }\n    thirdPartyInventoryContext {\n      isTpiBlock\n "
                 "     __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PriceDisplayInfoIrene on "
                 "PriceDisplayInfoIrene {\n  badges {\n    name {\n      translation\n      __typename\n    }\n    tooltip "
                 "{\n      translation\n      __typename\n    }\n    style\n    identifier\n    __typename\n  }\n  "
                 "chargesInfo {\n    translation\n    __typename\n  }\n  displayPrice {\n    copy {\n      translation\n    "
                 "  __typename\n    }\n    amountPerStay {\n      amount\n      amountRounded\n      amountUnformatted\n    "
                 "  currency\n      __typename\n    }\n    __typename\n  }\n  priceBeforeDiscount {\n    copy {\n      "
                 "translation\n      __typename\n    }\n    amountPerStay {\n      amount\n      amountRounded\n      "
                 "amountUnformatted\n      currency\n      __typename\n    }\n    __typename\n  }\n  rewards {\n    "
                 "rewardsList {\n      termsAndConditions\n      amountPerStay {\n        amount\n        amountRounded\n   "
                 "     amountUnformatted\n        currency\n        __typename\n      }\n      breakdown {\n        "
                 "productType\n        amountPerStay {\n          amount\n          amountRounded\n          "
                 "amountUnformatted\n          currency\n          __typename\n        }\n        __typename\n      }\n     "
                 " __typename\n    }\n    rewardsAggregated {\n      amountPerStay {\n        amount\n        "
                 "amountRounded\n        amountUnformatted\n        currency\n        __typename\n      }\n      copy {\n   "
                 "     translation\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  "
                 "useRoundedAmount\n  discounts {\n    amount {\n      amount\n      amountRounded\n      "
                 "amountUnformatted\n      currency\n      __typename\n    }\n    name {\n      translation\n      "
                 "__typename\n    }\n    description {\n      translation\n      __typename\n    }\n    itemType\n    "
                 "productId\n    __typename\n  }\n  excludedCharges {\n    excludeChargesAggregated {\n      copy {\n       "
                 " translation\n        __typename\n      }\n      amountPerStay {\n        amount\n        amountRounded\n "
                 "       amountUnformatted\n        currency\n        __typename\n      }\n      __typename\n    }\n    "
                 "excludeChargesList {\n      chargeMode\n      chargeInclusion\n      chargeType\n      amountPerStay {\n  "
                 "      amount\n        amountRounded\n        amountUnformatted\n        currency\n        __typename\n    "
                 "  }\n      __typename\n    }\n    __typename\n  }\n  taxExceptions {\n    shortDescription {\n      "
                 "translation\n      __typename\n    }\n    longDescription {\n      translation\n      __typename\n    }\n "
                 "   __typename\n  }\n  __typename\n}\n\nfragment BookerExperienceData on SearchResultProperty {\n  "
                 "bookerExperienceContentUIComponentProps {\n    ... on BookerExperienceContentLoyaltyBadgeListProps {\n    "
                 "  badges {\n        variant\n        key\n        title\n        popover\n        logoSrc\n        "
                 "logoAlt\n        __typename\n      }\n      __typename\n    }\n    ... on "
                 "BookerExperienceContentFinancialBadgeProps {\n      paymentMethod\n      backgroundColor\n      "
                 "hideAccepted\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SearchMetadata on "
                 "SearchMeta {\n  availabilityInfo {\n    hasLowAvailability\n    unavailabilityPercent\n    "
                 "totalAvailableNotAutoextended\n    __typename\n  }\n  boundingBoxes {\n    swLat\n    swLon\n    neLat\n  "
                 "  neLon\n    type\n    __typename\n  }\n  childrenAges\n  dates {\n    checkin\n    checkout\n    "
                 "lengthOfStayInDays\n    __typename\n  }\n  destId\n  destType\n  guessedLocation {\n    destId\n    "
                 "destType\n    destName\n    __typename\n  }\n  maxLengthOfStayInDays\n  nbRooms\n  nbAdults\n  "
                 "nbChildren\n  userHasSelectedFilters\n  customerValueStatus\n  isAffiliateBookingOwned\n  "
                 "affiliatePartnerChannelId\n  affiliateVerticalType\n  geniusLevel\n  __typename\n}\n\nfragment "
                 "SearchResultsBreadcrumb on SearchResultsBreadcrumb {\n  destId\n  destType\n  name\n  "
                 "__typename\n}\n\nfragment SorterFields on SorterOption {\n  type: name\n  captionTranslationTag {\n    "
                 "translation\n    __typename\n  }\n  tooltipTranslationTag {\n    translation\n    __typename\n  }\n  "
                 "isSelected: selected\n  __typename\n}\n\nfragment OneOfThreeDeal on OneOfThreeDeal {\n  id\n  uuid\n  "
                 "winnerHotelId\n  winnerBlockId\n  priceDisplayInfoIrene {\n    displayPrice {\n      amountPerStay {\n    "
                 "    amountRounded\n        amountUnformatted\n        __typename\n      }\n      __typename\n    }\n    "
                 "__typename\n  }\n  locationInfo {\n    name\n    inName\n    destType\n    __typename\n  }\n  "
                 "destinationType\n  commonFacilities {\n    id\n    name\n    __typename\n  }\n  tpiParams {\n    "
                 "wholesalerCode\n    rateKey\n    rateBlockId\n    bookingRoomId\n    supplierId\n    __typename\n  }\n  "
                 "properties {\n    priceDisplayInfoIrene {\n      priceBeforeDiscount {\n        amountPerStay {\n         "
                 " amountRounded\n          amountUnformatted\n          __typename\n        }\n        __typename\n      "
                 "}\n      displayPrice {\n        amountPerStay {\n          amountRounded\n          amountUnformatted\n  "
                 "        __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    "
                 "basicPropertyData {\n      id\n      name\n      pageName\n      photos {\n        main {\n          "
                 "highResUrl {\n            absoluteUrl\n            __typename\n          }\n          __typename\n        "
                 "}\n        __typename\n      }\n      location {\n        address\n        countryCode\n        "
                 "__typename\n      }\n      reviews {\n        reviewsCount\n        totalScore\n        __typename\n      "
                 "}\n      __typename\n    }\n    blocks {\n      thirdPartyInventoryContext {\n        rateBlockId\n       "
                 " rateKey\n        wholesalerCode\n        tpiRoom {\n          bookingRoomId\n          __typename\n      "
                 "  }\n        supplierId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  "
                 "__typename\n}\n\nfragment TripTypesData on TripTypes {\n  beach {\n    isBeachUfi\n    "
                 "isEnabledBeachUfi\n    __typename\n  }\n  ski {\n    isSkiExperience\n    isSkiScaleUfi\n    __typename\n "
                 " }\n  __typename\n}\n\nfragment ZeroResultsSection on ZeroResultsSection {\n  title {\n    text\n    "
                 "__typename\n  }\n  primaryAction {\n    text {\n      text\n      __typename\n    }\n    action {\n      "
                 "name\n      __typename\n    }\n    __typename\n  }\n  paragraphs {\n    text\n    __typename\n  }\n  "
                 "type\n  __typename\n}\n\nfragment PreviousSearches on PreviousSearch {\n  childrenAges\n  "
                 "__typename\n}\n\nfragment FrontierThemes on FrontierTheme {\n  id\n  name\n  selected\n  "
                 "__typename\n}\n\nfragment MerchRegionIrene on MerchComponentsResultIrene {\n  regions {\n    id\n    "
                 "components {\n      ... on PromotionalBannerIrene {\n        promotionalBannerCampaignId\n        "
                 "contentArea {\n          title {\n            ... on PromotionalBannerSimpleTitleIrene {\n              "
                 "value\n              __typename\n            }\n            __typename\n          }\n          subTitle {"
                 "\n            ... on PromotionalBannerSimpleSubTitleIrene {\n              value\n              "
                 "__typename\n            }\n            __typename\n          }\n          caption {\n            ... on "
                 "PromotionalBannerSimpleCaptionIrene {\n              value\n              __typename\n            }\n     "
                 "       ... on PromotionalBannerCountdownCaptionIrene {\n              campaignEnd\n              "
                 "__typename\n            }\n            __typename\n          }\n          buttons {\n            "
                 "variant\n            cta {\n              ariaLabel\n              text\n              targetLanding {\n  "
                 "              ... on OpenContextSheet {\n                  sheet {\n                    ... on "
                 "WebContextSheet {\n                      title\n                      body {\n                        "
                 "items {\n                          ... on ContextSheetTextItem {\n                            text\n      "
                 "                      __typename\n                          }\n                          ... on "
                 "ContextSheetList {\n                            items {\n                              text\n             "
                 "                 __typename\n                            }\n                            __typename\n      "
                 "                    }\n                          __typename\n                        }\n                  "
                 "      __typename\n                      }\n                      buttons {\n                        "
                 "variant\n                        cta {\n                          text\n                          "
                 "ariaLabel\n                          targetLanding {\n                            ... on "
                 "DirectLinkLanding {\n                              urlPath\n                              queryParams {\n "
                 "                               name\n                                value\n                              "
                 "  __typename\n                              }\n                              __typename\n                 "
                 "           }\n                            ... on LoginLanding {\n                              stub\n     "
                 "                         __typename\n                            }\n                            ... on "
                 "DeeplinkLanding {\n                              urlPath\n                              queryParams {\n   "
                 "                             name\n                                value\n                                "
                 "__typename\n                              }\n                              __typename\n                   "
                 "         }\n                            ... on ResolvedLinkLanding {\n                              url\n "
                 "                             __typename\n                            }\n                            "
                 "__typename\n                          }\n                          __typename\n                        "
                 "}\n                        __typename\n                      }\n                      __typename\n        "
                 "            }\n                    __typename\n                  }\n                  __typename\n        "
                 "        }\n                ... on SearchResultsLandingIrene {\n                  destType\n               "
                 "   destId\n                  checkin\n                  checkout\n                  nrAdults\n            "
                 "      nrChildren\n                  childrenAges\n                  nrRooms\n                  filters {"
                 "\n                    name\n                    value\n                    __typename\n                  "
                 "}\n                  __typename\n                }\n                ... on DirectLinkLandingIrene {\n     "
                 "             urlPath\n                  queryParams {\n                    name\n                    "
                 "value\n                    __typename\n                  }\n                  __typename\n                "
                 "}\n                ... on LoginLandingIrene {\n                  stub\n                  __typename\n     "
                 "           }\n                ... on DeeplinkLandingIrene {\n                  urlPath\n                  "
                 "queryParams {\n                    name\n                    value\n                    __typename\n      "
                 "            }\n                  __typename\n                }\n                ... on SorterLandingIrene "
                 "{\n                  sorterName\n                  __typename\n                }\n                "
                 "__typename\n              }\n              __typename\n            }\n            __typename\n          "
                 "}\n          __typename\n        }\n        designVariant {\n          ... on "
                 "DesktopPromotionalFullBleedImageIrene {\n            image: image {\n              id\n              url("
                 "width: 814, height: 138)\n              alt\n              overlayGradient\n              "
                 "primaryColorHex\n              __typename\n            }\n            colorScheme\n            "
                 "signature\n            __typename\n          }\n          ... on DesktopPromotionalImageLeftIrene {\n     "
                 "       imageOpt: image {\n              id\n              url(width: 248, height: 248)\n              "
                 "alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            "
                 "}\n            colorScheme\n            signature\n            __typename\n          }\n          ... on "
                 "DesktopPromotionalImageRightIrene {\n            imageOpt: image {\n              id\n              url("
                 "width: 248, height: 248)\n              alt\n              overlayGradient\n              "
                 "primaryColorHex\n              __typename\n            }\n            colorScheme\n            "
                 "signature\n            __typename\n          }\n          ... on MdotPromotionalFullBleedImageIrene {\n   "
                 "         image: image {\n              id\n              url(width: 358, height: 136)\n              "
                 "alt\n              overlayGradient\n              primaryColorHex\n              __typename\n            "
                 "}\n            colorScheme\n            signature\n            __typename\n          }\n          ... on "
                 "MdotPromotionalImageLeftIrene {\n            imageOpt: image {\n              id\n              url("
                 "width: 128, height: 128)\n              alt\n              overlayGradient\n              "
                 "primaryColorHex\n              __typename\n            }\n            colorScheme\n            "
                 "signature\n            __typename\n          }\n          ... on MdotPromotionalImageRightIrene {\n       "
                 "     imageOpt: image {\n              id\n              url(width: 128, height: 128)\n              alt\n "
                 "             overlayGradient\n              primaryColorHex\n              __typename\n            }\n    "
                 "        colorScheme\n            signature\n            __typename\n          }\n          ... on "
                 "MdotPromotionalImageTopIrene {\n            imageOpt: image {\n              id\n              url(width: "
                 "128, height: 128)\n              alt\n              overlayGradient\n              primaryColorHex\n      "
                 "        __typename\n            }\n            colorScheme\n            signature\n            "
                 "__typename\n          }\n          ... on MdotPromotionalIllustrationLeftIrene {\n            imageOpt: "
                 "image {\n              id\n              url(width: 200, height: 200)\n              alt\n              "
                 "overlayGradient\n              primaryColorHex\n              __typename\n            }\n            "
                 "colorScheme\n            signature\n            __typename\n          }\n          ... on "
                 "MdotPromotionalIllustrationRightIrene {\n            imageOpt: image {\n              id\n              "
                 "url(width: 200, height: 200)\n              alt\n              overlayGradient\n              "
                 "primaryColorHex\n              __typename\n            }\n            colorScheme\n            "
                 "signature\n            __typename\n          }\n          __typename\n        }\n        __typename\n     "
                 " }\n      ... on MerchCarouselIrene @include(if: $carouselLowCodeExp) {\n        carouselCampaignId\n     "
                 "   __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
    }


def check_info(
        response: requests.Response,
        entered_city: str,
        entered_check_in: str,
        entered_check_out: str,
        entered_selected_currency: str,
        entered_num_adult: int,
        entered_num_children: int,
        entered_num_room: int) -> tuple:
    """
    Get total page number.
    :param response: Requests response.
    :param entered_city: City where the hotels are located.
    :param entered_check_in: Check-in date.
    :param entered_check_out: Check-out date.
    :param entered_selected_currency: Currency of the room price.
    :param entered_num_adult: Number of adults.
    :param entered_num_children: Number of children.
    :param entered_num_room: Number of rooms.
    :return: Tuple of data.
    """
    if response.status_code == 200:
        data = response.json()
        total_page_num = data['data']['searchQueries']['search']['pagination']['nbResultsTotal']

        data_mapping = {
            "city": data['data']['searchQueries']['search']['breadcrumbs'][2]['name'],
            "check_in": data['data']['searchQueries']['search']['flexibleDatesConfig']['dateRangeCalendar']['checkin'][
                0],
            "check_out":
                data['data']['searchQueries']['search']['flexibleDatesConfig']['dateRangeCalendar']['checkout'][0],
            "num_adult": data['data']['searchQueries']['search']['searchMeta']['nbAdults'],
            "num_children": data['data']['searchQueries']['search']['searchMeta']['nbChildren'],
            "num_room": data['data']['searchQueries']['search']['searchMeta']['nbRooms'],
            "selected_currency": data['data']['searchQueries']['search']['results'][0]['blocks'][0]['finalPrice'][
                'currency']
        }

        for key, value in data_mapping.items():
            if locals()[f"entered_{key}"] != value:
                logger.error(
                    f"Error {key.replace('_', ' ').title()} not match: {locals()[f'entered_{key}']} != {value}")
                raise SystemExit(
                    f"Error {key.replace('_', ' ').title()} not match: {locals()[f'entered_{key}']} != {value}")

        return total_page_num, data_mapping
    else:
        logger.error(f"Error: {response.status_code}")


def scrape_graphql(
        city: str = None,
        check_in: str = None,
        check_out: str = None,
        selected_currency: str = None,
        group_adults: int = 1,
        num_rooms: int = 1,
        group_children: int = 0,
        hotel_filter: bool = False) -> pd.DataFrame:
    """
    Scrape hotel data from GraphQL endpoint.
    :param city: City where the hotels are located.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param selected_currency: Currency of the room price.
    :param group_adults: Number of adults.
                        Default is 1.
    :param num_rooms: Number of rooms.
                    Default is 1.
    :param group_children: Number of children.
                        Default is 0.
    :param hotel_filter: If True, scrape only hotel properties, else scrape all properties.
                        Default is False.
    :return: Pandas DataFrame with hotel data.
    """
    logger.info("Start scraping data from GraphQL endpoint")
    logger.info(f"City: {city} | Check-in: {check_in} | Check-out: {check_out} | Currency: {selected_currency}")
    logger.info(f"Adults: {group_adults} | Children: {group_children} | Rooms: {num_rooms}")
    logger.info(f"Only hotel properties: {hotel_filter}")

    if check_in and check_out and selected_currency:
        # GraphQL endpoint URL
        url = f'https://www.booking.com/dml/graphql?selected_currency={selected_currency}'
        headers = get_header()
        graphql_query = get_graphql_query(city=city, check_in=check_in, check_out=check_out, group_adults=group_adults,
                                          group_children=group_children, num_rooms=num_rooms, hotel_filter=hotel_filter)

        response = requests.post(url, headers=headers, json=graphql_query)

        total_page_num, hotel_data_dict = check_info(
            response, city, check_in, check_out, selected_currency, group_adults, group_children, num_rooms
        )
        logger.debug(f"Total page number: {total_page_num}")
        logger.debug(f"City: {hotel_data_dict['city']}")
        logger.debug(f"Check-in date: {hotel_data_dict['check_in']}")
        logger.debug(f"Check-out date: {hotel_data_dict['check_out']}")
        logger.debug(f"Number of adults: {hotel_data_dict['num_adult']}")
        logger.debug(f"Number of children: {hotel_data_dict['num_children']}")
        logger.debug(f"Number of rooms: {hotel_data_dict['num_room']}")
        logger.debug(f"Currency: {hotel_data_dict['selected_currency']}")

        df_list = []
        logger.info("Scraping data from GraphQL endpoint...")
        for offset in range(0, total_page_num, 100):
            graphql_query = get_graphql_query(city=city, check_in=check_in, check_out=check_out,
                                              group_adults=group_adults,
                                              group_children=group_children, num_rooms=num_rooms,
                                              hotel_filter=hotel_filter,
                                              page_offset=offset)
            response = requests.post(url, headers=headers, json=graphql_query)

            if response.status_code == 200:
                data = response.json()
                hotel_data_list: list = data['data']['searchQueries']['search']['results']

                extract_hotel_data(df_list, hotel_data_list)
            else:
                logger.error(f"Error: {response.status_code}")

        df = concat_df_list(df_list)
        return transform_data_in_df(check_in, city, df)
    else:
        logger.warning("Error: check_in, check_out and selected_currency are required")


def concat_df_list(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatenate a list of Pandas Dataframes.
    :param df_list: A list of Pandas Dataframes.
    :return: Pandas DataFrame.
    """
    logger.info("Concatenate a list of Pandas Dataframes")
    if df_list:
        df_main = pd.concat(df_list)
        return df_main
    else:
        logger.warning("No data was scraped.")
        return pd.DataFrame()


def transform_data_in_df(check_in, city, dataframe) -> pd.DataFrame:
    """
    Transform data in DataFrame.
    :param check_in: Check-in date.
    :param city: City where the hotels are located.
    :param dataframe: Pandas DataFrame to be transformed.
    :return: Pandas DataFrame.
    """
    if not dataframe.empty:
        logger.info("Add City column to DataFrame")
        dataframe['City'] = city
        logger.info("Add Date column to DataFrame")
        dataframe['Date'] = check_in
        logger.info("Add AsOf column to DataFrame")
        dataframe['AsOf'] = datetime.datetime.now()

        logger.info("Remove duplicate rows from the DataFrame based on 'Hotel' column")
        df_filtered = dataframe.drop_duplicates(subset='Hotel').copy()

        logger.info("Convert columns to numeric values")
        df_filtered.loc[:, 'Price'] = pd.to_numeric(df_filtered['Price'], errors='coerce')
        df_filtered.loc[:, 'Review'] = pd.to_numeric(df_filtered['Review'], errors='coerce')

        # Drop rows where any of the 'Hotel', 'Review', 'Price' columns are None or NaN
        logger.info("Dropping rows where 'Hotel', 'Review', or 'Price' columns are None or NaN")
        df_filtered = df_filtered.dropna(subset=['Hotel', 'Review', 'Price'])

        logger.info("Dropping rows where 'Review', or 'Price' columns are 0")
        df_filtered = df_filtered[(df_filtered['Price'] != 0) & (df_filtered['Review'] != 0)]

        logger.info("Calculate the Price/Review ratio")
        df_filtered.loc[:, 'Price/Review'] = df_filtered['Price'] / df_filtered['Review']
        return df_filtered
    else:
        logger.warning("Dataframe is empty. No data was scraped.")
        return dataframe


def extract_hotel_data(df_list: list, hotel_data_list: list) -> None:
    """
    Extract data from a list of hotel data.
    :param df_list: A list to store Pandas Dataframes.
    :param hotel_data_list: List of results.
    :return:
    """
    logger.debug("Extracting data...")
    for hotel_data in hotel_data_list:
        logger.debug("Initialize lists to store extracted data")
        display_names = []
        review_scores = []
        final_prices = []
        for key, val in hotel_data.items():
            if key == "displayName":
                if val:
                    display_names.append(val['text'])
                else:
                    display_names.append(None)

            if key == "basicPropertyData":
                if val:
                    review_scores.append(val['reviewScore']['score'])
                else:
                    review_scores.append(None)

            if key == "blocks":
                if val:
                    final_prices.append(val[0]['finalPrice']['amount'])
                else:
                    final_prices.append(None)

        logger.debug("Create a Pandas Dataframe to store extracted data")
        df = pd.DataFrame({
            "Hotel": display_names,
            "Review": review_scores,
            "Price": final_prices
        })

        logger.debug("Append dataframe to a df_list")
        df_list.append(df)


def save_scraped_data(
        dataframe: pd.DataFrame,
        city: str = None,
        check_in: str = None,
        check_out: str = None,
        save_dir='scraped_hotel_data') -> None:
    """
    Save scraped data to CSV files in the given directory.
    The CSV files directory is created automatically if it doesn't exist.
    The default CSV files directory name is depended on the default value of 'save_dir' parameter.
    :param dataframe: Pandas DataFrame.
    :param city: City where the hotels are located.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param save_dir: Directory to save the scraped data as CSV.
                    Default is 'scraped_hotel_data_csv' folder.
    :return: None
    """
    logger.info("Saving scraped data...")
    if not dataframe.empty:
        logger.info('Save data to Excel')
        try:
            # Attempt to create the directory
            os.makedirs(save_dir)
            logger.info(f'Created {save_dir} directory')
        except FileExistsError:
            # If the directory already exists, log a message and continue
            logger.error(f'FileExistsError: {save_dir} directory already exists')

        if city and check_in and check_out:
            file_path = os.path.join(save_dir, f'{city}_hotel_data_{check_in}_to_{check_out}.xlsx')
            dataframe.to_excel(file_path, index=False)
            logger.info("Data saved to Excel")
        else:
            logger.warning("Cannot save data to Excel. "
                           "please enter city, check-in or check-out date. ")
    else:
        logger.warning('The dataframe is empty. No data to save')


if __name__ == '__main__':
    city = 'Osaka'
    check_in = '2024-08-16'
    check_out = '2024-08-17'
    group_adults = 1
    num_rooms = 1
    group_children = 0
    selected_currency = 'USD'
    hotel_filter = True

    df = scrape_graphql(city=city, check_in=check_in, check_out=check_out, group_adults=group_adults,
                        group_children=group_children, num_rooms=num_rooms, hotel_filter=hotel_filter,
                        selected_currency=selected_currency)

    save_scraped_data(dataframe=df, city=city, check_in=check_in, check_out=check_out)

package com.yrssn.service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.yrssn.mapper.SportsDataMapper;
import com.yrssn.pojo.sportsData;
import com.yrssn.service.SportsDataService;
import org.springframework.stereotype.Service;

@Service
public class SportsDataSeviceIml extends ServiceImpl<SportsDataMapper, sportsData> implements  SportsDataService{



}

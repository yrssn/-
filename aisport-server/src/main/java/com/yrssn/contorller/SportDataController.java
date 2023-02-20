package com.yrssn.contorller;


import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.yrssn.pojo.User;
import com.yrssn.pojo.sportsData;
import com.yrssn.service.SportsDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
public class SportDataController {
    @Autowired
    SportsDataService SportsDataSeviceIml;

    @RequestMapping("/sportdata")
    @ResponseBody
    public List<sportsData> test(String suid){
        QueryWrapper<sportsData> queryWrapper=new QueryWrapper();
        queryWrapper.eq("suid",suid);
        return SportsDataSeviceIml.list(queryWrapper);
    }

    @RequestMapping("/addsportdata")
    @ResponseBody
    public int test1(sportsData sportsData){
        if (SportsDataSeviceIml.save(sportsData)){
            return 1;
        }else
            return 0;


    }
    @RequestMapping("/deletedata")
    @ResponseBody
    public int test2(Integer sid){
        if (SportsDataSeviceIml.removeById(sid))
            return 1;
        else
            return 0;

    }
    @RequestMapping("/queryalldata")
    @ResponseBody
    public List<sportsData> test3(){
        return SportsDataSeviceIml.list();

    }

}

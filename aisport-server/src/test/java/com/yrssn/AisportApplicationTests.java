package com.yrssn;

import com.yrssn.mapper.SportsDataMapper;
import com.yrssn.pojo.sportsData;
import com.yrssn.service.SportsDataService;
import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import javax.annotation.Resource;
import java.util.List;

@Slf4j
@SpringBootTest
class AisportApplicationTests {
    @Resource
    SportsDataMapper sportsDataMapper;
    @Autowired
    SportsDataService sportsDataService;
    @Test
    void contextLoads(){}
    @Test
    void test1(){
        // 创建密码解析器
                BCryptPasswordEncoder bCryptPasswordEncoder = new BCryptPasswordEncoder();

        // 对密码进行加密
                String atguigu = bCryptPasswordEncoder.encode("atguigu");

        // 打印加密之后的数据
                System.out.println("加密之后数据：\t"+atguigu);

        //判断原字符加密后和加密之前是否匹配
                boolean result = bCryptPasswordEncoder.matches("atguigu", atguigu);
                // 打印比较结果
                System.out.println("比较结果：\t"+result);


    }



}

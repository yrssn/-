package com.yrssn;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;


@SpringBootApplication()
@MapperScan("com.yrssn.mapper")
public class AisportApplication {

    public static void main(String[] args) {
        SpringApplication.run(AisportApplication.class, args);
    }

}
